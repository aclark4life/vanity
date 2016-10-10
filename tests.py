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
        normalized = vanity.normalize("dJaNgO")
        self.assertEqual(normalized, "Django")

    def testNone(self):
        normalized = vanity.normalize(None)
        self.assertEqual(normalized, "none")

    def testEmpty(self):
        """
        TODO: this test is rather slow to run,
        perhaps normalize could be refactored to check this
        and kick out faster.
        """
        normalized = vanity.normalize("")
        self.assertEqual(normalized, "")

if __name__ == '__main__':
    unittest.main()
