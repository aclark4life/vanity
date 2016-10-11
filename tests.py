import unittest

import vanity


class test_normalize(unittest.TestCase):
    """
    A test class for the normalize method.
    """

    def test_fake_package(self):
        self.assertRaises(ValueError,
                          vanity.normalize,
                          "FAKEPACKAGE1@!")
        self.assertRaises(ValueError,
                          vanity.normalize,
                          "1337INoscopeyou")

    def test_django(self):
        normalized = vanity.normalize("dJaNgO")
        self.assertEqual(normalized, "Django")

    def test_none(self):
        normalized = vanity.normalize(None)
        self.assertEqual(normalized, "none")

    def test_flask(self):
        normalized = vanity.normalize("fLaSk")
        self.assertEqual(normalized, "Flask")

    def test_space_string(self):
        normalized = vanity.normalize("               Flask                ")
        self.assertEqual(normalized, "               Flask                ")

    def test_empty(self):
        """
        TODO: this test is rather slow to run,
        perhaps normalize could be refactored to check this
        and kick out faster.
        """
        normalized = vanity.normalize("")
        self.assertEqual(normalized, "")

if __name__ == '__main__':
    unittest.main()
