###############################################################################
# Copyright (C) 2011-2012 Alex Clark                                          #
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

"""fetch download counts from PyPI"""

# Based on https://github.com/collective/Products.PloneSoftwareCenter\
# /blob/master/Products/PloneSoftwareCenter/pypi.py

from collections import deque
#import blessings
try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection
import locale
import optparse
import sys
import time
try:
    import xmlrpc.client as xmlrpc
except ImportError:  # Python 2
    import xmlrpclib as xmlrpc

client = xmlrpc.ServerProxy('http://pypi.python.org/pypi')
try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    pass
#term = blessings.Terminal()


def by_two(source):
    out = []
    for x in source:
        out.append(x)
        if len(out) == 2:
            yield out
            out = []


def normalise_project(name):
    http = HTTPConnection('pypi.python.org')
    http.request('HEAD', '/simple/%s/' % name)
    r = http.getresponse()
    if r.status not in (200, 301):
        raise ValueError(r.reason)
    return r.getheader('location', name).split('/')[-1]


def package_releases(packages):
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


def downloads_total(package, verbose=False):
    total = 0
    items = []
    for urls, data in release_data([package]):
        for url in urls:
            if verbose:
                filename = url['filename']
                downloads = url['downloads']
                upload_time = time.strftime('    %Y-%m-%d',  # XXX Would
                    # like to print '%s(key)s' % url but upload_time
                    # is a DateTime object
                    url['upload_time'].timetuple())
                items.append('%s %s %8s' % (filename, upload_time,
                    locale.format("%d", downloads, grouping=True)))

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


def main():
    """
    Run the vanity
    """

    parser = optparse.OptionParser()
    parser.add_option('-q', '--quiet', action="store_false", dest="verbose",
                      default=True,
                      help='do not print results for individual uploads')

    options, packages = parser.parse_args()
    for package in packages:
        try:
            project = normalise_project(package)
        except ValueError:
            project = sys.argv[1]
            parser.error('No such module or package %r' % project)

        total = downloads_total(project, verbose=options.verbose)

        if total != 0:
#            print term.bold('%s' % project), 'has been downloaded'\
#                , term.bold('%s' % locale.format("%d", total, grouping=True))\
#                , 'times!'
            print('%s has been downloaded %s times!'
                  % (project, locale.format("%d", total, grouping=True)))
        else:
#            print 'No downloads for', term.bold('%s' % project)
            print('No downloads for %s' % project)

if __name__ == '__main__':
    main()
    sys.exit(0)
