import re
import argparse
from bs4 import BeautifulSoup as bs
from typing import List, Set, Dict, Tuple, Optional
from genanki import genanki
from crawler import Database


def getVocabulary(html: str) -> str:
    html = bs(html, 'html.parser')

    h1 = html.find("h1")
    word = h1.contents[0]
    if word is None:
        h2 = html.find("h2")
        word = h2.contents[0]

    return word

def editHTMLWord(html) -> str: 
    soup = bs(html, 'html.parser')
    content = soup.find("div", {"id":"entryContent"})
    if content:
        for div in content.find_all("div", {"id": "ring-links-box"}):
            div.decompose()
        for div in content.find_all("div", {'class':'symbols'}): 
            div.decompose()
        for div in content.find_all("div", {"class": "am-default contentslot"}):
            div.decompose()

    return str(content)


def cloze(html: str, words: List[str]) -> str:
    html = bs(html, 'html.parser')
    for id, word in enumerate(words):
        if len(word) >= 3: 
            search = r'\b%s' % word
        else: 
            search = r'\b%s\b' % word

        for text in html.find_all(text = re.compile(search)):
            editor = re.sub(search, "{{c%d::%s}}" % (id + 1, word), text)
            text.replace_with(editor)

    return str(html)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='crawl.py')
    parser.add_argument('--name', type=str, help="Name anki deck")
    parser.add_argument('--dataPath', type=str, help="path Data")
    opt = parser.parse_args()
    print(opt)
    name = opt.name

    with open('static/script.js') as file: 
        script = file.read()

    with open('static/layout.css') as file: 
        css = file.read()

    my_model = genanki.Model(220072021, 
                            name,
                            fields=[{'name': 'front'},{'name': 'back'}],
                            templates=[
                                {
                                'name': 'Oxford dictionary',
                                'qfmt': '{{type:cloze:front}} {{cloze:front}}',
                                'afmt': '{{type:cloze:front}} {{back}}' + script,
                                },
                            ], 
                            css=css, 
                            model_type=1
                            )

    deck = genanki.Deck(320072021, name)

    database = Database(opt.dataPath)

    for _, url, page, _ in database.getData("%definition%"):
        word = getVocabulary(page)
        front = cloze(page, [word])
        note = genanki.Note(model=my_model, fields=[front, page])
        deck.add_note(note)        

    genanki.Package(deck).write_to_file('%s.apkg' % name)