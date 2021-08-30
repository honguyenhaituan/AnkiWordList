import os
from typing import List
import requests
import base64
from bs4 import BeautifulSoup as bs
from helper import *
from threading import Thread, Lock
from queue import Queue, Empty

import traceback
import logging

log = logging.getLogger('Main.threadPool')

class Downloader(Thread): 
    def __init__(self, manager: DownloadManager):
        Thread.__init__(self)
        self.manager = manager
        self.daemon = True
        self.stateStop = False
        self.start()

    def stop(self): 
        self.stateStop = True

    def run(self):
        while True: 
            if self.stateStop: break
            try: 
                func, args, kwargs = self.manager.getTask(timeout=1)
            except Empty: 
                continue

            try: 
                self.manager.increaseDownloader()
                result = func(*args, **kwargs)
                self.manager.decreaseDownloader()
                if result: 
                    self.manager.handleResult(*result)
                
                self.manager.handleTaskDone()
            except Exception as e: 
                log.critical(str(e))
                log.critical(traceback.format_exc())


# class DownloadManager: 
#     def __init__(self, projectName: str, seed: List[str]):
#         self.projectName = projectName
#         self.dataPath = os.path.join(projectName, 'data')
        
#         self.queueFile = os.path.join(projectName, 'queue.txt')
#         self.crawledUrlFile = os.path.join(projectName, 'crawledUrl.txt')
#         self.crawledContentFile = os.path.join(projectName, "crawledContent.txt")

#     def boot(self):
#         createProjectDir(self.projectName)
#         createDataFiles(self.projectName)

#         self.queue = file_to_set(self.queueFile)
#         self.crawledUrl = file_to_set(self.crawledFile)
#         self.crawledContent = file_to_set(self.crawledContentFile)

#     def addUrls(self, urls: List[str]) -> None: 
#         for url in urls: 
#             if self.isCrawledUrl(url): continue
#             self.queue.add(url)

#     def getUrl(self) -> str: 
#         return self.queue.get()
        

#     def isCrawledUrl(self, url: str) -> bool: 
#         return url in self.crawledUrl

#     def isCrawledContent(self, content: str) -> bool:
#         hashValue = base64.b64encode(hash(content).to_bytes(8, byteorder='big'))
#         return hashValue in self.crawledContent

#     def downloadPage(self, url: str, save: bool = True): 
#         try: 
#             headers = requests.utils.default_headers()
#             headers.update({'User-Agent': 'My User Agent 1.0',})
#             page = requests.get(url, headers=headers)
            
#             if save:
#                 with open(os.path.join(self.dataPath, url + ".html"), "w") as f:
#                     f.write(page)
    
#             return page.text
#         except Exception as e:
#             print(str(e))
#             return None

#     def findUrl(self, url: str, page: str) -> List[str]:
#         #TODO: change hardcode
#         html = bs(page, 'html.parser')
#         links = html.find("ul", {"class":"top-g"})

#         ans = []
#         for link in links.find_all("a"):
#             href = link["href"].encode('utf8')
#             if not href.startswith('http'):
#                 href = os.path.join(url, href)

#             ans.append(href)

#         return ans
        
#     def crawlPage(self, url): 
#         if self.isCrawledUrl(url): return
        
#         page = self.downloadPage(url)
#         if (page is None) or (self.isCrawledContent(page)): return

#         urls = self.findUrl(page)
#         self.addUrls(urls)