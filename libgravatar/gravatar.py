import re,hashlib
from . import exceptions as e
from http.httpconnector import HttpConnector

class Gravatar:

    GRAVATAR_PATH="/xmlrpc?user="
    GRAVATAR_HOST="secure.gravatar.com"

    def __init__(self,email=None):
       if email is not None:
            self.setEmail(email)
            self.hash=self.getHash()

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
        return 'https://{1}{2}{3}'.format(GRAVATAR_HOST,GRAVATAR_PATH,self.hash)

    def connect(self): #TODO Create a session with a time limit and connect to the host
        """API Endpoint: https://secure.gravatar.com/xmlrpc?user=[email_hash]
        It is mandatory that you connect to secure.gravatar.com, and that you do so over HTTPS.
        This is for the safety of our mutual users. The email_hash GET parameter is the md5 hash of the users email
        address after it has been lowercased, and trimmed."""
        try:
            if self.email is None:
                raise Exception
            url=self.getUrl()

        except Exception:
            raise e.PyGravatarConnectException('Couldn\'t connect with email'+self.email)

    def request_image(self):
        AVATAR_URL='http://www.gravatar.com/avatar/{1}'.format(self.getHash())
        httpConnector=HttpConnector(AVATAR_URL)
        img=httpConnector.get(AVATAR_URL)

