import datetime
import urlparse
import time

class Throttle:

    def __init__(self,delay):
        self.delay = delay
        self.domains = {}

    def wait(self,url):
        #ParseResult(scheme='http', netloc='example.webscraping.com', path='/', params='', query='', fragment='')
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if(self.delay > 0 and last_accessed is not None):
            sleep_sec = self.delay - (datetime.datatime.now()-last_accessed).seconds
            if( sleep_sec > 0 ):
                time.sleep(sleep_sec)

        self.domains[domain] = datetime.datetime.now()