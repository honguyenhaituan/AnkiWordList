import traceback
import re
import logging

import requests

log = logging.getLogger('Main.WebPage')


class WebPage(object):

    def __init__(self, url):
        self.url = url
        self.pageSource = None
        self.customeHeaders()

    def fetch(self, retry=2, proxies=None):
        try:
            response = requests.get(self.url, headers=self.headers)#, timeout=10, prefetch=False, proxies=proxies)
            if self._isResponseAvaliable(response):
                self._handleEncoding(response)
                self.pageSource = response.text
                return True
            else:
                log.warning('Page not avaliable. Status code:%d URL: %s \n' % (
                    response.status_code, self.url) )
        except Exception as e:
            if retry > 0:
                return self.fetch(retry-1)
            else:
                log.debug(str(e) + ' URL: %s \n' % self.url)
        return None

    def customeHeaders(self, **kargs):      
        self.headers = requests.utils.default_headers()
        self.headers.update({'User-Agent': 'My User Agent 1.0',})
        self.headers.update(kargs)

    def getDatas(self):
        return self.url, self.pageSource

    def _isResponseAvaliable(self, response):
        if response.status_code == requests.codes.ok:
            if 'html' in response.headers['Content-Type']:
                return True
        return False

    def _handleEncoding(self, response):
        if response.encoding == 'ISO-8859-1':
            charset_re = re.compile("((^|;)\s*charset\s*=)([^\"']*)", re.M)
            charset=charset_re.search(response.text) 
            charset=charset and charset.group(3) or None 
            response.encoding = charset