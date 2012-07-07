import xmlrpclib, httplib


class ProxiedTransport(xmlrpclib.Transport):

    def __init__(self,proxy=None):
        self.set_proxy(proxy)
        super(ProxiedTransport)

    def set_proxy(self, proxy):
        self.checkProxy(proxy)
        self.proxy = proxy
    def make_connection(self, host):
        self.realhost = host
        h = httplib.HTTP(self.proxy)
        return h
    def send_request(self, connection, handler, request_body):
        connection.putrequest("POST", 'http://{1}{2}'.format(self.realhost, handler))
    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)

