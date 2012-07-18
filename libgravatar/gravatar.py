import re,hashlib,exceptions as e,const.PyGravConst as c
from logger.coloredLogger import ColoredLogger
from http.httpconnector import HttpConnector
from xmlrpc.xmlrpcConnector import xmlRpcConnector
import cache

APIKEY = 'apikey'
PASSWORD='password'
GRAVATAR_PATH='/xmlrpc?user='
GRAVATAR_HOST="https://secure.gravatar.com"
GRAVATAR_RATING=c.rating
GRAVATAR_ERRORS=c.ERRORS

class Gravatar:

    def __init__(self,email=None,options={},proxy=None,force_http=False,connect=False):
        if email is not None:
            self.setEmail(email)
            self.hash=self.getHash()
            if connect:
                self.connect()
        self.proxy=proxy
        if force_http:
            GRAVATAR_HOST.replace('https','http')
        self.logger=ColoredLogger('PyGravatar')
        self.cache=None
        self.options=options
        self.buildAuthKeys(options) #builds auth attribute from options dictionary

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

    def request_image(self):
        httpConnector=HttpConnector(self.proxy)
        return httpConnector.get(self.get_avatar_url())

    #===================================================================================
    #                               API Methods
    #===================================================================================
    def grav_exists(self):
        """grav.exists - check whether a hash has a gravatar
            @param  $args['hashes'] an array of hashes to check
            @param	$args['apikey'] || $args[PASSWORD] for authentication
            @return array (
                hash => (bool)exists,
            )"""
        pass

    def grav_addesses(self):
        """grav.addresses - get a list of addresses for this account
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return array (
                address => array (
                rating        => (int)rating,
                                      userimage     => (int)userimage,
                                                            userimage_url => (int)userimage_url
            )
            )"""
        pass

    @cache.Cache()
    def grav_userimages(self):
        """"grav.userimages - return an array of userimages for this account
            @param  $args['apikey'] || $args[PASSWORD] for authentication
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
        @param  $args['apikey'] || $args[PASSWORD] for authentication
        @return (bool)false on failure, (string)userimage on success
        """
        pass

    def grav_saveUrl(self):
        """grav.saveUrl - Read an image via its URL and save that as a userimage for this account
        @param  (string)$args['url'] a full url to an image
        @param  (int)$args['rating'] 0:g, 1:pg, 2:r, 3:x
        @param  $args['apikey'] || $args[PASSWORD] for authentication
        @return (bool)false on failure, (string)userimage on success"""
        pass

    def grav_useUserImage(self):
        """grav.useUserimage - use a userimage as a gravatar for one of more addresses on this account
            @param  (string)$args['userimage'] The userimage you wish to use
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return array(
                address => (bool)status
            )"""
        pass

    def grav_removeImage(self):
        """grav.removeImage - remove the userimage associated with one or more email addresses
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return array(
                address => (bool)status
            )"""
        pass

    def grav_deleteUserImage(self):
        """grav.deleteUserimage - remove a userimage from the account and any email addresses with which it is associated
            @param  (string)$args['userimage'] The userimage you wish to remove from the account
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return (bool)status
        """


    def grav_test(self):#TODO: move this method to the GravatarTest.py
        """grav.test - a test function
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return (mixed)$args
        """
        pass

    #===================================================================================
    #                               Auxiliary Methods
    #===================================================================================

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
        return '{1}{2}{3}'.format(GRAVATAR_HOST,GRAVATAR_PATH,self.hash)

    def get_avatar_url(self):
        return '{1}/avatar/{2}'.format(GRAVATAR_HOST,self.getHash())

    def getAvatarTag(self):
        """Return avatar url inside an img tag"""
        return "<img src=\"{1}\"/>".format(self.get_avatar_url)
    
    def _filterAuthKeys(self,options): #filter method
        return dict([(k,v) for k,v in options.iteritems() if k in (PASSWORD,'api','apikey','api_key','pass')])

    def normalizeAuthOptions(self,dictionary):
        for k,v in dictionary.iteritems:
            if k in ('api', APIKEY,'api_key'):
                dictionary[APIKEY] = dictionary.pop(k)
            elif k in (PASSWORD,'pass'):
                dictionary[PASSWORD] = dictionary.pop(k)

    def buildAuthKeys(self,options):
        filtered_options=self._filterAuthKeys(options)
        self.auth=self.normalizeAuthOptions(filtered_options)
