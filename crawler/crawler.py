
import re
import time
import logging
import traceback

from bs4 import BeautifulSoup 
from collections import deque
from urllib.parse import urljoin, urlparse

from .database import Database
from .webPage import WebPage
from .threadpool import ThreadPool

log = logging.getLogger('Main.crawler')

class Crawler(object):
    def __init__(self, depth, dbFile, numThread, seed):
        self.depth = depth  
        self.currentDepth = 1  
        self.database =  Database(dbFile)
        self.threadPool = ThreadPool(numThread)  
        self.visitedHrefs = set()   
        self.unvisitedHrefs = deque()    
        self.unvisitedHrefs.append(seed) 
        self.isCrawling = False

    def start(self):
        print('\nStart Crawling\n')
        if not self._isDatabaseAvaliable():
            print('Error: Unable to open database file.\n')
        else:
            self.isCrawling = True
            self.threadPool.startThreads() 
            while self.currentDepth < self.depth + 1:
                self._assignCurrentDepthTasks()
                while self.threadPool.getTaskLeft():
                    time.sleep(8)
                print('Depth %d Finish. Totally visited %d links. \n' 
                    % (self.currentDepth, len(self.visitedHrefs)))

                log.info('Depth %d Finish. Total visited Links: %d\n'
                    % (self.currentDepth, len(self.visitedHrefs)))
                self.currentDepth += 1
            self.stop()

    def stop(self):
        self.isCrawling = False
        self.threadPool.stopThreads()
        self.database.close()

    def getAlreadyVisitedNum(self):
        return len(self.visitedHrefs) - self.threadPool.getTaskLeft()

    def _assignCurrentDepthTasks(self):
        while self.unvisitedHrefs:
            url = self.unvisitedHrefs.popleft()
            self.threadPool.putTask(self._taskHandler, url) 
            self.visitedHrefs.add(url)  
 
    def _taskHandler(self, url):
        webPage = WebPage(url)
        if webPage.fetch():
            self._saveTaskResults(webPage)
            self._addUnvisitedHrefs(webPage)

    def _saveTaskResults(self, webPage):
        url, pageSource = webPage.getDatas()
        try:
            if self.keyword:
                if re.search(self.keyword, pageSource, re.I):
                    self.database.saveData(url, pageSource, self.keyword) 
            else:
                self.database.saveData(url, pageSource)
        except Exception as e:
            log.error(' URL: %s ' % url + traceback.format_exc())

    def _addUnvisitedHrefs(self, webPage):
        url, pageSource = webPage.getDatas()
        hrefs = self._getAllHrefsFromPage(url, pageSource)
        for href in hrefs:
            if self._isHttpOrHttpsProtocol(href):
                if not self._isHrefRepeated(href):
                    self.unvisitedHrefs.append(href)

    def _getAllHrefsFromPage(self, url, pageSource):
        hrefs = []
        soup = BeautifulSoup(pageSource)
        results = soup.find_all('a',href=True)
        for a in results:
            href = a.get('href').encode('utf8')
            if not href.startswith('http'):
                href = urljoin(url, href)
            hrefs.append(href)
        return hrefs

    def _isHttpOrHttpsProtocol(self, href):
        protocal = urlparse(href).scheme
        if protocal == 'http' or protocal == 'https':
            return True
        return False

    def _isHrefRepeated(self, href):
        if href in self.visitedHrefs or href in self.unvisitedHrefs:
            return True
        return False

    def _isDatabaseAvaliable(self):
        if self.database.isConn():
            return True
        return False