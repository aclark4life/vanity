"""utils to fetch download counts from PyPI"""

from collections import deque, defaultdict
import logging
import sys
import xmlrpclib

logger = logging.getLogger('vanity')

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
        mcall.package_releases(package,True)
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


if __name__ == '__main__':
    for urls, data in release_data([sys.argv[1]]):
#        print 'DATA: %s\n' % data
        print 'URLS: %s\n' % urls[0]['downloads']
