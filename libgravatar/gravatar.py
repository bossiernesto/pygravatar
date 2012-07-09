import re,hashlib
import exceptions as e
from logger.coloredLogger import ColoredLogger
from http.httpconnector import HttpConnector
from xmlrpc.xmlrpcConnector import xmlRpcConnector

class Gravatar:

    GRAVATAR_PATH='/xmlrpc?user='
    GRAVATAR_HOST="https://secure.gravatar.com"


    GRAVATAR_RATING={0:'g', 1:'pg', 2:'r', 3:'x'}
    GRAVATAR_ERRORS={}

    def __init__(self,email=None,proxy=None,force_http=False,connect=False):
        if email is not None:
            self.setEmail(email)
            self.hash=self.getHash()
            if connect:
                self.connect()
        self.proxy=proxy
        if force_http:
            self.GRAVATAR_HOST.replace('https','http')
        self.logger=ColoredLogger('PyGravatar')

    def setEmail(self,email):
        self.email=email

    def normalizeEmail(self):
        """Normalize Email, removing whitespaces and applying lowercase to email"""
        self.setEmail(re.sub(r'\s', '',self.email))

    def getHash(self):
        """Get MD5 Digest to authenticate and get to all API functionality"""
        m=hashlib.md5()
        m.update(self.email)
        return m.hexdigest()

    def getUrl(self):
        if self.hash is None:
            self.hash=self.getHash()
        return '{1}{2}{3}'.format(self.GRAVATAR_HOST,self.GRAVATAR_PATH,self.hash)

    def connect(self): #TODO Create a session with a time limit and connect to the host
        """API Endpoint: https://secure.gravatar.com/xmlrpc?user=[email_hash]
        It is mandatory that you connect to secure.gravatar.com, and that you do so over HTTPS.
        This is for the safety of our mutual users. The email_hash GET parameter is the md5 hash of the users email
        address after it has been lowercased, and trimmed"""
        try:
            if self.email is None:
                raise Exception
            url=self.getUrl()
            self.rpc=xmlRpcConnector(url,self.proxy)
        except Exception:
            raise e.PyGravatarConnectException('Couldn\'t connect with email'+self.email)

    def get_avatar_url(self):
        return '{1}/avatar/{2}'.format(self.GRAVATAR_HOST,self.getHash())

    def getAvatarTag(self):
        """Return avatar url inside an img tag"""
        return "<img src=\"{1}\"/>".format(self.get_avatar_url)

    def request_image(self):
        httpConnector=HttpConnector(self.proxy)
        img=httpConnector.get(self.get_avatar_url())

    def grav_exists(self):
        """grav.exists - check whether a hash has a gravatar
            @param  $args['hashes'] an array of hashes to check
            @param	$args['apikey'] || $args['password'] for authentication
            @return array (
                hash => (bool)exists,
            )"""
        pass

    def grav_addesses(self):
        """grav.addresses - get a list of addresses for this account
            @param  $args['apikey'] || $args['password'] for authentication
            @return array (
                address => array (
                rating        => (int)rating,
                                      userimage     => (int)userimage,
                                                            userimage_url => (int)userimage_url
            )
            )"""
        pass


    def grav_userimages(self):
        """"grav.userimages - return an array of userimages for this account
            @param  $args['apikey'] || $args['password'] for authentication
            @return array (
                userimage => array(
                (int)rating, // 0:g, 1:pg, 2:r, 3:x
                (string)url,
            )
            )"""
        pass

    def grav_saveData(self):
        """grav.saveData - Save binary image data as a userimage for this account
        @param  (string)$args['data'] a base64_encode()d image
        @param  (int)$args['rating'] 0:g, 1:pg, 2:r, 3:x
        @param  $args['apikey'] || $args['password'] for authentication
        @return (bool)false on failure, (string)userimage on success
        """
        pass

    def grav_saveUrl(self):
        """grav.saveUrl - Read an image via its URL and save that as a userimage for this account
        @param  (string)$args['url'] a full url to an image
        @param  (int)$args['rating'] 0:g, 1:pg, 2:r, 3:x
        @param  $args['apikey'] || $args['password'] for authentication
        @return (bool)false on failure, (string)userimage on success"""
        pass

    def grav_useUserImage(self):
        """grav.useUserimage - use a userimage as a gravatar for one of more addresses on this account
            @param  (string)$args['userimage'] The userimage you wish to use
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args['password'] for authentication
            @return array(
                address => (bool)status
            )"""
        pass

    def grav_removeImage(self):
        """grav.removeImage - remove the userimage associated with one or more email addresses
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args['password'] for authentication
            @return array(
                address => (bool)status
            )"""
        pass

    def grav_deleteUserImage(self):
        """grav.deleteUserimage - remove a userimage from the account and any email addresses with which it is associated
            @param  (string)$args['userimage'] The userimage you wish to remove from the account
            @param  $args['apikey'] || $args['password'] for authentication
            @return (bool)status
        """


    def grav_test(self):#TODO: move this method to the GravatarTest.py
        """grav.test - a test function
            @param  $args['apikey'] || $args['password'] for authentication
            @return (mixed)$args
        """
        pass

