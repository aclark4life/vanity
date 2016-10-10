import unittest

import vanity

class testNormalize(unittest.TestCase):
    """
    A test class for the normalize method.
    """

    def testFakePackage(self):
        self.assertRaises(ValueError, 
                          vanity.normalize, 
                          "FAKEPACKAGE1@!")

    def testDjango(self):
        n = vanity.normalize("dJaNgO")
        self.assertEqual(n, "Django")

    def testNone(self):
        n = vanity.normalize(None)
        self.assertEqual(n, "none")

    def testEmpty(self):
        """
        Note: this test is rather slow to run, 
        perhaps normalize could be refactored to check this
        and kick out faster.
        """
        n = vanity.normalize("")
        self.assertEqual(n, "")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testNormalize))
    return suite

if __name__ == '__main__':
    suite = suite()
    unittest.TextTestRunner().run(suite())

    
