import xmlrpclib


class xmlRpcConnector(xmlrpclib.ServerProxy):
    """uri [,options] -> a logical connection to an XML-RPC server

        uri is the connection point on the server, given as
        scheme://host/target.

        If the target part and the slash preceding it are both omitted,
        "/RPC2" is assumed.

        The following options can be given as keyword arguments:

            transport: a transport factory
            encoding: the request encoding (default is UTF-8)

        All 8-bit strings passed to the server proxy are assumed to use
        the given encoding.
        """
    def call(self,name,*args,**kwargs):
        """This function is used to call any method provided by the Gravatar api"""
        #TODO: do a type checking of **kwargs
        pass




