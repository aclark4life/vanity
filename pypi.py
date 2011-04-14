############################################################################### 
# Copyright (C) 2011 Alex Clark                                               #
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

# Based on http://svn.plone.org/svn/collective/Products.PloneSoftwareCenter/\
# trunk/Products/PloneSoftwareCenter/pypi.py

from collections import deque
import sys
import xmlrpclib

client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')


def by_two(source):
    out = []
    for x in source:
        out.append(x)
        if len(out) == 2:
            yield out
            out = []


def package_releases(packages):
    mcall = xmlrpclib.MultiCall(client)
    called_packages = deque()
    for package in packages:
        mcall.package_releases(package, True)
        called_packages.append(package)
        if len(called_packages) == 100:
            result = mcall()
            mcall = xmlrpclib.MultiCall(client)
            for releases in result:
                yield called_packages.popleft(), releases
    result = mcall()
    for releases in result:
        yield called_packages.popleft(), releases


def release_data(packages):
    mcall = xmlrpclib.MultiCall(client)
    i = 0
    for package, releases in package_releases(packages):
        for version in releases:
            mcall.release_urls(package, version)
            mcall.release_data(package, version)
            i += 1
            if i % 50 == 49:
                result = mcall()
                mcall = xmlrpclib.MultiCall(client)
                for urls, data in by_two(result):
                    yield urls, data
    result = mcall()
    for urls, data in by_two(result):
        yield urls, data


def main():
    usage = 'Usage: vanity [my.package]'
    if len(sys.argv) >= 2 and len(sys.argv) < 3:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print usage
        else:
            total = 0
            for urls, data in release_data([sys.argv[1]]):
                if not urls == []:
                    total += urls[0]['downloads']
            if total != 0:
                print 'Package `%s` has been downloaded %d times!\n' % (
                    sys.argv[1], total)
            else:
                print 'No downloads. Are you sure `%s` exists?\n' % (
                    sys.argv[1])
    else:
        print usage

if __name__ == '__main__':
    main()
