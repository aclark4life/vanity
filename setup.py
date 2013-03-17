from setuptools import setup
import os


VERSION = '1.2.4'


setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    classifiers=[
        'Programming Language :: Python :: 3.3',
    ],
    description='Easy access to package download statistics \
        from the Python Package Index, via the command line',
    entry_points={
        'console_scripts': 'vanity=vanity:vanity',
    },
    include_package_data=True,
    keywords='analytics python package index statistics',
    license='GPL',
    long_description=(open('README.rst').read() + open(
        os.path.join('docs', 'HISTORY.txt')).read()),
    name='vanity',
    py_modules=[
        'vanity',
    ],
    test_suite='tests.TestSuite',
    url='https://github.com/aclark4life/vanity',
    version=VERSION,
    zip_safe=True,
)
