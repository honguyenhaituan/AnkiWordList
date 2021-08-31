# AnkiWordList

## A Web crawler.  
* Start from the url and crawl the web pages with a specified depth.  
* Save the pages into database.  
* Support multi-threading.    


Usage
-------------
```shell
crawl.py -url URL -depth DEPTH [--logfile FILE] [--loglevel {1,2,3,4,5}]
               [--thread NUM] [--dbfile FILE] [--key KEYWORD] [--testself]
```

Optional arguments:
-------------
```shell
  -url URL              Specify the begin url
  -depth DEPTH          Specify the crawling depth
  --logfile FILE        The log file path, Default: spider.log
  --loglevel {1,2,3,4,5}
                        The level of logging details. Larger number record
                        more details. Default:3
  --thread NUM          The amount of threads. Default:10
  --dbfile FILE         The SQLite file path. Default:data.sql
  --key KEYWORD         The keyword for crawling. Default: None. For more than
                        one word, quote them. example: --key 'Hello world'
  --testself            Crawler self test

```

## Anki Deck Wordlist.
1. Crawl wordlist from oxford learner's dictionary
```
python crawl.py --depth 2 --url "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
```  
2. Covert database to anki deck
```
python anki_deck.py --name Name --dataPath data
