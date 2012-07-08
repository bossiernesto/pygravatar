import xmlrpclib,re,proxyTransport
from ..exceptions import ProxyFormatException

class xmlRpcConnector():
    """rpcUrl [,options] -> a logical connection to an XML-RPC server

        rpcUrl is the connection point on the server, given as
        scheme://host/target.

        If the target part and the slash preceding it are both omitted,
        "/RPC2" is assumed.

        The following options can be given as keyword arguments:

            proxy: configure connector if behind a Proxy Server, parameter should be like "host:port@user:password"
        """

    def init(self,rpcUrl,proxy=None):
        if proxy is not None:
            self.checkProxy(proxy)
            self.transport=proxyTransport.ProxiedTransport(proxy)
        else:
            self.transport=None
        self.rpc=xmlrpclib.ServerProxy(rpcUrl,transport=self.transport)

    def checkProxy(self,proxy):
        """Check proxy format "host:port@user:password" """
        regex=re.compile(r'\S+:[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)@\S+:\S+') #Simple RegEx to match the proxy definition
        if regex.match(proxy) is None:
            raise ProxyFormatException('Invalid proxy configuration format, should be like host:port@user:password')

    def call(self,name,*args,**kwargs):
        """This function is used to call any method provided by the Gravatar api"""
        try:
            arguments=kwargs
            return getattr(self.rpc,name)(*arguments)
        except Exception,e:
            pass




