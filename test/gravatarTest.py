from unittest import TestCase
from libgravatar import gravatar


class GravatarTest(TestCase):

    NORMALIZED_EMAIL="myemail@gmail.com"

    def setUp(self):
        self.email='myEmail@gmail.Com '
        self.pyGravApi=gravatar.Gravatar()
        self.pyGravApi.setEmail(self.email)

    def getNormalizedEmail(self):
        self.assertEquals(self.pyGravApi.normalizeEmail(),NORMALIZED_EMAIL)

    def getHash(self):
        self.assertEqual(self.pyGravApi.getHash(),'')#TODO: get md5 of the NORMALIZED_EMAIL to compare with pygravatar

