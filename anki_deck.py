import re
from bs4 import BeautifulSoup as bs
from pathlib import Path
from typing import List, Set, Dict, Tuple, Optional


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
    with open('static/script.js') as file: 
        script = file.read()

    with open('static/layout.css') as file: 
        script = file.read()