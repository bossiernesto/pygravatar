import urllib2,contextlib


class HttpConnector():

    def __init__(self,proxy=None):
        if proxy is not None:
            self.proxyHandler=urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(self.proxyHandler)
        else:
            self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')]

    def get(self,url):
        link=self.normalizeUrl(url)
        with contextlib.closing(self.opener.open(link)) as r:
            broken_html=r.read()
        return broken_html

    def normalizeUrl(self,url):
        """Normalize URL and clean it"""
        return urllib2.quote(url.encode('utf-8'), safe="%/:=&?~#+!$,;'@()*[]")

    def getImage(self,url):
        raw=self.get(url)





