import unittest
from utils import ordereddict

class testOrderedDict(unittest.TestCase):


    def setUp(self):
        self.dictionary=ordereddict.OrderedDict()
        #Set some values
        self.dictionary[4]="aa"
        self.dictionary[21]="333"
        self.dictionary.__setitem__(2,"3334")

    def testHasKey(self):
        self.dictionary[1]="aaa"
        self.assertTrue(self.dictionary.has_key(1))

    def testsetAndPrint(self):
        self.dictionary[6]="aa"
        self.assertEqual(4,len(self.dictionary))


    def testMerge(self):
        newdict={1:'kkk',4:"aa"}
        self.dictionary.merge(newdict)
        self.assertEqual(4,len(self.dictionary))

    def testInverse(self):
        self.dictionary.reverse_dictionary()
        self.assertEqual(4,self.dictionary.__getitem__("aa"))
