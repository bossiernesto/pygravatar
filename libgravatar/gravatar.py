import re,hashlib,exceptions as e,const.PyGravConst as c
from logger.coloredLogger import ColoredLogger
from http.httpconnector import HttpConnector
from xmlrpc.xmlrpcConnector import xmlRpcConnector
import cache,base64

APIKEY = 'apikey'
PASSWORD='password'
GRAVATAR_PATH='/xmlrpc?user='
GRAVATAR_HOST="https://secure.gravatar.com"
GRAVATAR_RATING=c.rating

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
    @cache.Cache()
    def grav_exists(self,hashes):
        """grav.exists - check whether a hash has a gravatar
            @param  $args['hashes'] an array of hashes to check
            @param	$args['apikey'] || $args[PASSWORD] for authentication
            @return array (
                hash => (bool)exists,
            )"""
        pass

    @cache.Cache()
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

    def grav_saveData(self,dataIn,ratingIn):
        """grav.saveData - Save binary image data as a userimage for this account
        @param  (string)$args['data'] a base64_encode()d image
        @param  (int)$args['rating'] 0:g, 1:pg, 2:r, 3:x
        @param  $args['apikey'] || $args[PASSWORD] for authentication
        @return (bool)false on failure, (string)userimage on success
        """
        encoded=base64.encodestring(dataIn)
        encoded_rating=self.getRating(ratingIn)
        userimage=self.rpc.call('saveData',self,data=encoded,rating=encoded_rating)
        if not userimage:
            raise PyGravException('')
        return userimage


    def grav_saveUrl(self,imageUrl,Rating):
        """grav.saveUrl - Read an image via its URL and save that as a userimage for this account
        @param  (string)$args['url'] a full url to an image
        @param  (int)$args['rating'] 0:g, 1:pg, 2:r, 3:x
        @param  $args['apikey'] || $args[PASSWORD] for authentication
        @return (bool)false on failure, (string)userimage on success"""
        id=self.rpc.call('saveUrl',self,image=imageUrl,rating=self.getRating(Rating))
        if not id:
            raise PyGravException('')
        return id

    def grav_useUserImage(self,userimageID,addresses):
        """grav.useUserimage - use a userimage as a gravatar for one of more addresses on this account
            @param  (string)$args['userimage'] The userimage you wish to use
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return array(
                address => (bool)status
            )"""
        return self.check_address_return(self.rpc.call('useUserimage',self,userimage=userimageID,addresses=addresses))

    def grav_removeImage(self,addresses):
        """grav.removeImage - remove the userimage associated with one or more email addresses
            @param  (array)$args['addresses'] A list of the email addresses you wish to use this userimage for
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return array(
                address => (bool)status
            )"""
        return  self.check_address_return(self.rpc.call('removeImage',self,addresses=addresses))

    def grav_deleteUserImage(self,userimageID):
        """grav.deleteUserimage - remove a userimage from the account and any email addresses with which it is associated
            @param  (string)$args['userimage'] The userimage you wish to remove from the account
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return (bool)status
        """
        return bool(self.rpc.call('deleteUserimage',self,userimage=userimageID))

    def grav_test(self):#TODO: move this method to the GravatarTest.py
        """grav.test - a test function
            @param  $args['apikey'] || $args[PASSWORD] for authentication
            @return (mixed)$args
        """
        return self.rpc.call('test',self)['response']

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
        return '{0}{1}{2}'.format(GRAVATAR_HOST,GRAVATAR_PATH,self.hash)

    def get_avatar_url(self):
        return '{0}/avatar/{1}'.format(GRAVATAR_HOST,self.getHash())

    def getAvatarTag(self):
        """Return avatar url inside an img tag"""
        return "<img src=\"{0}\"/>".format(self.get_avatar_url)
    
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

    def getAuthToken(self):
        if self.auth is None:
            self.buildAuthKeys(self.options)
        return self.auth

    def check_address_return(self,responses):
        for email,status in responses.iteritems():
            if not status:
                raise PyGravException('Failed call to {0}'.format('removeImage'))
        return responses