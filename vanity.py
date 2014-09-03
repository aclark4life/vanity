###############################################################################
# Copyright (C) 2011-2014 Alex Clark                                          #
#                                                                             #
# This program is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU General Public License                 #
# as published by the Free Software Foundation; either version 2              #
# of the License, or (at your option) any later version.                      #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program; if not, write to the Free Software                 #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,   #
# USA.                                                                        #
###############################################################################

"""
Get package download statistics from PyPI.
"""

# Based on https://github.com/collective/Products.PloneSoftwareCenter\
# /blob/master/Products/PloneSoftwareCenter/pypi.py

from __future__ import print_function
from collections import deque
try:
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection
import argparse
import locale
import time
try:
    import xmlrpc.client as xmlrpc
except ImportError:  # Python 2
    import xmlrpclib as xmlrpc

client = xmlrpc.ServerProxy('https://pypi.python.org/pypi')
try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    pass
FORMAT = '%Y-%m-%d'
OPERATOR = '=='


def by_two(source):
    """
    """
    out = []
    for x in source:
        out.append(x)
        if len(out) == 2:
            yield out
            out = []


def downloads_total(package, verbose=True, version=None):
    """
    """
    total = 0
    items = []
    for urls, data in release_data([package]):
        for url in urls:
            filename = url['filename']
            downloads = url['downloads']
            downloads = locale.format("%d", downloads, grouping=True)
            upload_time = url['upload_time'].timetuple()
            upload_time = time.strftime(FORMAT, upload_time)
            if version == data['version'] or not version:
                item = '%s    %s    %9s' % (
                    filename, upload_time, downloads)
                items.append(item)
                total += url['downloads']
    if verbose and items != []:
        items.reverse()
        # http://stackoverflow.com/questions/873327/\
        # pythons-most-efficient-way-to-choose-longest-string-in-list
        longest = len(max(items, key=len))
        for item in items:
            print(item.rjust(longest))
        print('-' * longest)
    # Don't break api
    return total


def normalise_package(name):
    """
    """
    http = HTTPSConnection('pypi.python.org')
    http.request('HEAD', '/pypi/%s/' % name)
    r = http.getresponse()
    if r.status not in (200, 301):
        raise ValueError(r.reason)
    return r.getheader('location', name).split('/')[-1]


def package_releases(packages):
    """
    """
    mcall = xmlrpc.MultiCall(client)
    called_packages = deque()
    for package in packages:
        mcall.package_releases(package, True)
        called_packages.append(package)
        if len(called_packages) == 100:
            result = mcall()
            mcall = xmlrpc.MultiCall(client)
            for releases in result:
                yield called_packages.popleft(), releases
    result = mcall()
    for releases in result:
        yield called_packages.popleft(), releases


def release_data(packages):
    """
    """
    mcall = xmlrpc.MultiCall(client)
    i = 0
    for package, releases in package_releases(packages):
        for version in releases:
            mcall.release_urls(package, version)
            mcall.release_data(package, version)
            i += 1
            if i % 50 == 49:
                result = mcall()
                mcall = xmlrpc.MultiCall(client)
                for urls, data in by_two(result):
                    yield urls, data
    result = mcall()
    for urls, data in by_two(result):
        yield urls, data


def vanity():
    """
    Get package download statistics from PyPI.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', help='package name', nargs='+')
    parser.add_argument('--quiet', help='verbosity', action='store_true')
    args = parser.parse_args()
    packages = args.package
    verbose = not(args.quiet)
    version = None
    grand_total = 0
    package_list = []
    for package in packages:
        if package.find(OPERATOR) >= 0:
            # Check for version spec
            package, version = package.split('==')
        try:
            package = normalise_package(package)
        except ValueError:
            parser.error('No such module or package %r' % package)
        total = downloads_total(package, version=version, verbose=verbose)
        if total != 0:
            if version:
                print(
                    '%s %s has been downloaded %s times!' % (
                    package, version, locale.format(
                        "%d", total, grouping=True)))
            else:
                print(
                    '%s has been downloaded %s times!' % (
                    package, locale.format("%d", total, grouping=True)))
        else:
            if version:
                print('No downloads for %s %s.' % (package, version))
            else:
                print('No downloads for %s.' % package)
        grand_total += total
        package_list.append(package)
    if len(package_list) > 1:
        # List packages like "a and b" or "a, b and c" or "a, b, c and d"
        package_string = (', '.join(package_list[:-1]) + " and " +
                          package_list[-1])
        print(
            "%s have been downloaded %s times!" % (
                package_string, locale.format(
                    "%d", grand_total, grouping=True)))

if __name__ == '__main__':
    vanity()
