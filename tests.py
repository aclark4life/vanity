import unittest
import mock
import datetime

import vanity


# mocks
def mock_single_release(url):
    return {'releases': {'1.0': ''}}


def mock_multi_release(url):
    return {'releases': {'2.0': '1', '1.0': 'a', '3.1': 'a', '1.5': ''}}


def mock_json_data(url):
    return {'releases':
            {'1.0': [{'filename': 'fake-package',
                      'downloads': 1,
                      'upload_time': '2016-10-12T03:00:42'}],
             '1.9': [{'filename': 'fake-package',
                      'downloads': 3,
                      'upload_time': '2016-10-13T09:01:00'}],
             '1.2': [{'filename': 'fake-package',
                      'downloads': 2,
                      'upload_time': '2016-10-13T02:10:08'}]
             },
            'info': {'version': '1.0'}}


def empty_release_info(package, json):
    return iter(())


def single_release_info(package, json):
    url = {'filename': 'fake-package',
           'downloads': 1,
           'upload_time': datetime.date(2016, 10, 13)}
    data = {'version': '1.0'}

    yield [url], data


def two_url_release_info(package, json):
    first_url = {'filename': 'fake-package',
                 'downloads': 1,
                 'upload_time': datetime.date(2016, 10, 13)}

    second_url = {'filename': 'fake-package two',
                  'downloads': 2,
                  'upload_time': datetime.date(2016, 10, 13)}

    data = {'version': '1.0'}

    yield [first_url, second_url], data


def mock_normalize(package):
    return package


# http://stackoverflow.com/q/21611559
def Any(object_type):
    class Any(object_type):
        def __eq__(self, other):
            return True
    return Any()


class TestGetJsonParsedData(unittest.TestCase):
    """
    A test class for the get_jsonparsed_data method.
    """

    def test_none(self):
        self.assertRaises(AttributeError,
                          vanity.get_jsonparsed_data,
                          None)

    def test_empty_string(self):
        self.assertRaises(ValueError,
                          vanity.get_jsonparsed_data,
                          '')

    @mock.patch('vanity.get_json_from_url', side_effect=mock_single_release)
    def test_single_release(self, mock_json_func):
        expected = {'1.0': ''}
        response = vanity.get_jsonparsed_data('fake url')

        mock_json_func.assert_called_with('fake url')
        self.assertEqual(response['releases'], expected)

    @mock.patch('vanity.get_json_from_url', side_effect=mock_multi_release)
    def test_multi_release_sorts(self, mock_json_func):
        expected = {'1.0': 'a', '1.5': '', '2.0': '1', '3.1': 'a'}
        response = vanity.get_jsonparsed_data('fake url')

        mock_json_func.assert_called_with('fake url')
        self.assertEqual(response['releases'], expected)


class TestCountDownloads(unittest.TestCase):
    """
    A test class for the count_downloads method.
    """

    mock_logger = mock.Mock()

    def setUp(self):
        self.old_logger = vanity.logger
        vanity.logger = self.mock_logger

    def tearDown(self):
        vanity.logger = self.old_logger

    @mock.patch('vanity.get_release_info', side_effect=empty_release_info)
    def test_count_empty(self, get_release_func):
        count = vanity.count_downloads(None)

        self.assertEqual(count, 0)

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_count_single(self, get_release_func):
        count = vanity.count_downloads('fake-package')

        self.assertEqual(count, 1)

    @mock.patch('vanity.get_release_info', side_effect=two_url_release_info)
    def test_count_multiple(self, get_release_func):
        count = vanity.count_downloads('fake-package')

        self.assertEqual(count, 3)

    @mock.patch('vanity.get_json_from_url', side_effect=mock_json_data)
    def test_count_json(self, get_json_func):
        expected_url = 'https://pypi.python.org/pypi/fake-package/json'
        count = vanity.count_downloads('fake-package',
                                       json=True)

        get_json_func.assert_called_with(expected_url)
        self.assertEqual(count, 6)

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_count_version(self, get_release_func):
        count = vanity.count_downloads('fake-package',
                                       version='1.1')

        self.assertEqual(count, 0)

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_bad_pattern(self, get_release_func):
        count = vanity.count_downloads('fake-package',
                                       pattern='real')

        self.assertEqual(count, 0)

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_good_pattern(self, get_release_func):
        count = vanity.count_downloads('fake-package',
                                       pattern='[Ff]ake')

        self.assertEqual(count, 1)

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_verbose_calls_debug(self, get_release_func):

        count = vanity.count_downloads('fake-package')

        self.assertEqual(count, 1)
        self.mock_logger.debug.assert_any_call(Any(str))

    @mock.patch('vanity.get_release_info', side_effect=single_release_info)
    def test_not_verbose_no_debug(self, get_release_func):
        self.mock_logger = mock.Mock()

        count = vanity.count_downloads('fake-package',
                                       verbose=False)

        self.assertEqual(count, 1)
        self.mock_logger.debug.assert_not_called()


class TestByTwo(unittest.TestCase):
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
        self.assertIsNone(result.get('bar.net'))


class TestNormalize(unittest.TestCase):
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


class TestVanity(unittest.TestCase):
    """
    A test class for the vanity method.
    """

    mock_logger = mock.Mock()

    def setUp(self):
        self.old_logger = vanity.logger
        vanity.logger = self.mock_logger

    def tearDown(self):
        vanity.logger = self.old_logger

    @mock.patch('vanity.normalize', side_effect=mock_normalize)
    @mock.patch('vanity.get_json_from_url', side_effect=mock_json_data)
    def test_vanity_count_downloads(self, mock_json_func, mock_norm_func):
        # NB: mocks are passed in reverse order
        expected_url = 'https://pypi.python.org/pypi/fake-package/json'

        vanity.vanity(packages=['fake-package'],
                      verbose=True,
                      json=True,
                      pattern=None)

        mock_norm_func.assert_called_with('fake-package')
        mock_json_func.assert_called_with(expected_url)
        self.mock_logger.debug.assert_any_call(
            '%s has been downloaded %s times!',
            'fake-package',
            '6')

    @mock.patch('vanity.normalize', side_effect=mock_normalize)
    @mock.patch('vanity.get_json_from_url', side_effect=mock_json_data)
    def test_vanity_version_downloads(self, mock_json_func, mock_norm_func):
        # NB: mocks are passed in reverse order
        expected_url = 'https://pypi.python.org/pypi/fake-package/json'

        vanity.vanity(packages=['fake-package==1.0'],
                      verbose=True,
                      json=True,
                      pattern=None)

        mock_norm_func.assert_called_with('fake-package')
        mock_json_func.assert_called_with(expected_url)
        self.mock_logger.debug.assert_any_call(
            '%s %s has been downloaded %s times!',
            'fake-package',
            '1.0',
            '6')

if __name__ == '__main__':
    unittest.main()
