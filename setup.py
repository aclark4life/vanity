from setuptools import setup
import os

VERSION = '1.2.4'

setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='Easy access to package download statistics \
        from the Python Package Index, via the command line',
    entry_points={
        'console_scripts': 'vanity = vanity:main',
    },
    include_package_data=True,
    long_description=(open('README.rst').read() + open(
        os.path.join('docs', 'HISTORY.txt')).read()),
    name='vanity',
    py_modules=[
        'vanity'
    ],
    url='https://github.com/aclark4life/vanity',
    version=VERSION,
)
