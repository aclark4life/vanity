import unittest

import vanity


class TestNormalize(unittest.TestCase):
    """
    A test class for the by_two method.
    """

    def test_none(self):
        input = iter(())

        result = {url: data for (url, data) in vanity.by_two(input)}

        self.assertEqual(result, {})

    def test_pairs_url_and_data(self):
        input = iter(['test.com', 'test data',
                      'foo.org', 'foo data',
                      'bar.net', 'bar data'])

        result = {url: data for (url, data) in vanity.by_two(input)}

        self.assertEqual(result['test.com'], 'test data')
        self.assertEqual(result['foo.org'], 'foo data')
        self.assertEqual(result['bar.net'], 'bar data')

    def test_odd_input(self):
        input = iter(['test.com', 'test data',
                      'foo.org', 'foo data',
                      'bar.net'])

        result = {url: data for (url, data) in vanity.by_two(input)}

        self.assertEqual(result['test.com'], 'test data')
        self.assertEqual(result['foo.org'], 'foo data')
        self.assertEqual(result.get('bar.net'), None)


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
        normalized = vanity.normalize("")
        self.assertEqual(normalized, "")

if __name__ == '__main__':
    unittest.main()
