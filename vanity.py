# -*- coding: utf-8 -*-

# Copyright (C) 2011-2016 Alex Clark
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.
"""Get package download statistics from PyPI."""

import argparse
import json
import locale
import logging
import re
import time

# For sorting XML-RPC results
from collections import OrderedDict, deque, namedtuple

# HTTPS connection for normalize function
try:
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

# PyPI's XML-RPC methods
# https://wiki.python.org/moin/PyPIXmlRpc
try:
    import xmlrpc.client as xmlrpc
except ImportError:  # Python 2
    import xmlrpclib as xmlrpc

PYPI_HOST = 'pypi.python.org'
PYPI_URL = 'https://%s/pypi' % PYPI_HOST
PYPI_JSON = '/'.join([PYPI_URL, '%s/json'])
PYPI_XML = xmlrpc.ServerProxy(PYPI_URL)

# Print numbers with commas
# http://stackoverflow.com/a/1823101
try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    pass

# Logger
# https://docs.python.org/3/howto/logging.html
logger = logging.getLogger('vanity')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# PyPI JSON
# http://stackoverflow.com/a/28786650
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def by_two(source):
    """Accept XMLRPC Multicall generator, and return items in pairs.

    @param source: Result of XMLRPC Multicall
    @type source: generator
    @r_param out: Items from generator, as namedtuple(url, data)
    @r_type out: namedtuple
    """
    release_info = namedtuple('release_info', ['urls', 'data'])
    it = iter(source)
    for urls in it:
        yield release_info(urls=urls, data=next(it))


def count_downloads(package,
                    verbose=True,
                    version=None,
                    json=False,
                    pattern=None):
    """Receive package details, retrieve and return download count.

    Call get_release_info() method to make requests to get package details,
    check for verbose and json toggles, debug for discrepancies,
    maintain a download count counter and return total number of downloads.

    @param package: Name of package to be retrieved.
    @type package: str
    @param verbose: Verbose Toggle
    @type verbose: bool
    @param version: Version number of package
    @type version: str
    @param json: JSON Toggle
    @type json: bool
    @param pattern: Regex pattern
    @type pattern: str
    @r_param count: Download count of package on PyPI
    @r_type count: int
    """
    count = 0
    items = []
    for urls, data in get_release_info([package], json=json):
        for url in urls:
            filename = url['filename']
            if pattern and not re.search(pattern, filename):
                continue
            downloads = url['downloads']
            downloads = locale.format("%d", downloads, grouping=True)
            if not json:
                upload_time = url['upload_time'].timetuple()
                upload_time = time.strftime('%Y-%m-%d', upload_time)
            else:
                # Convert 2011-04-14T02:16:55 to 2011-04-14
                upload_time = url['upload_time'].split('T')[0]
            if version == data['version'] or not version:
                item = '%s    %s    %9s' % (filename, upload_time, downloads)
                items.append(item)
                count += url['downloads']
    if verbose and items != []:
        items.reverse()
        # http://stackoverflow.com/questions/873327/\
        # pythons-most-efficient-way-to-choose-longest-string-in-list
        longest = len(max(items, key=len))
        for item in items:
            logger.debug(item.rjust(longest))
        logger.debug('-' * longest)
    return count


def get_json_from_url(url):
    """
    Returns content of url as json
    """
    response = urlopen(url)
    return json.loads(response.read().decode('utf-8'))


# http://stackoverflow.com/a/28786650
def get_jsonparsed_data(url):
    """Receive content of 'url', parse it as JSON, return the object.

    @param url: URL of package's JSON data
    @type url: str
    @r_param response: JSON data from the URL
    @r_type response: dict
    """
    response = get_json_from_url(url)

    sorted_releases = OrderedDict()
    for release in sorted(response['releases'].keys())[::-1]:
        sorted_releases[release] = response['releases'][release]
    response['releases'] = sorted_releases
    return response


def normalize(name):
    """Normalize and return correct package name, if specified incorrectly.

    Accept the package name, send a HTTP request to the relevant
    URL, check response for valid PyPI existence, return normalized name.

    @param name: The name of the package to be checked
    @type name: str
    @r_param normalized_name: Verified package name
    @r_type normalized_name: str
    """
    if name == "":
        return ""

    http = HTTPSConnection(PYPI_HOST)
    http.request('HEAD', '/pypi/%s/' % name)
    r = http.getresponse()
    if r.status not in (200, 301):
        raise ValueError(r.reason)
    normalized_name = r.getheader('location', name).split('/')[-1]
    return normalized_name


def get_releases(packages):
    """Retrieve and return package data via XMLRPC requests.

    @param packages: List of packages
    @type packages: list
    @r_param "called_packages.popleft()": Called package ame
    @r_type "called_packages.popleft()": str
    @r_param releases: Items from Multicall Generator Object
    @r_type releases: XMLRPC Proxy Object
    """
    mcall = xmlrpc.MultiCall(PYPI_XML)
    called_packages = deque()
    for package in packages:
        mcall.package_releases(package, True)
        called_packages.append(package)
        if len(called_packages) == 100:
            result = mcall()
            mcall = xmlrpc.MultiCall(PYPI_XML)
            for releases in result:
                yield called_packages.popleft(), releases
    result = mcall()
    for releases in result:
        yield called_packages.popleft(), releases


def get_release_info(packages, json=False):
    """Retrieve statistics for package passed in by calling other methods.

    Based on JSON toggle, retrieve package data as JSON or via XMLRPC requests
    and return the data.

    @param packages: List of package names
    @type packages: list
    @param json: JSON Toggle
    @type json: bool
    @r_param urls: Details of a particular release
    @r_type urls: dict
    @r_param data[info]/data: General information about package
    @r_type data[info]/data: dict
    """
    if json:
        for package in packages:
            data = get_jsonparsed_data(PYPI_JSON % package)
            for release in data['releases']:
                urls = data['releases'][release]
                yield urls, data['info']
        return

    mcall = xmlrpc.MultiCall(PYPI_XML)

    i = 0
    for package, releases in get_releases(packages):
        for version in releases:
            mcall.release_urls(package, version)
            mcall.release_data(package, version)
            i += 1
            if i % 50 == 49:
                result = mcall()
                mcall = xmlrpc.MultiCall(PYPI_XML)
                for urls, data in by_two(result):

                    yield urls, data

    result = mcall()
    for urls, data in by_two(result):
        yield urls, data


def vanity(packages, verbose, json):
    """Parse args, verify package, retrieve details, return download count."""
    version = None
    grand_total = 0
    package_list = []
    for package in packages:
        if package.find('==') >= 0:
            package, version = package.split('==')
        try:
            package = normalize(package)
        except ValueError:
            logger.debug('No such module or package %r', package)
            continue

        # Count downloads
        total = count_downloads(package,
                                json=json,
                                version=version,
                                verbose=verbose,
                                pattern=args.pattern)
        if total != 0:
            if version:
                logger.debug('%s %s has been downloaded %s times!',
                             package, version, locale.format("%d",
                                                             total,
                                                             grouping=True))
            else:
                logger.debug('%s has been downloaded %s times!',
                             package, locale.format("%d",
                                                    total,
                                                    grouping=True))
        else:
            if version:
                logger.debug('No downloads for %s %s.', package, version)
            else:
                logger.debug('No downloads for %s.', package)
        grand_total += total
        package_list.append(package)
    if len(package_list) > 1:
        package_string = (
            ', '.join(package_list[:-1]) + " and " + package_list[-1])
        logger.debug("%s have been downloaded %s times!",
                     package_string, locale.format("%d",
                                                   grand_total,
                                                   grouping=True))

    logger.debug("\n\n\t *** Note: PyPI stats are broken again; we're now"
                 "waiting for warehouse. https://github.com/aclark4life/"
                 "vanity/issues/22 ***\n\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', help='pypi package name', nargs='+')
    parser.add_argument('-q',
                        '--quiet',
                        help='only show total downloads',
                        action='store_true')
    parser.add_argument('-j',
                        '--json',
                        help='use pypi json api instead of xmlrpc',
                        action='store_true')
    parser.add_argument('-p',
                        '--pattern',
                        help='only show files matching a regex pattern')
    args = parser.parse_args()

    vanity(packages=args.package,
           verbose=not (args.quiet),
           json=args.json)
