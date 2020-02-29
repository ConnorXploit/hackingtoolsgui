import hackingtools as ht
import unittest2 as unittest

class MyTest(unittest.TestCase):

    def test_ht_rsa_getRandomKeypair(self):
        module = ht.getModule('rsa')
        self.assertIsInstance(module.getRandomKeypair(3), tuple)

if __name__ == "__main__":
    unittest.main()