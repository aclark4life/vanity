from setuptools import setup
import os

VERSION = '2.2.2'

setup(author='Alex Clark',
      author_email='aclark@aclark.net',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      description='Get package download statistics from PyPI',
      entry_points={
          'console_scripts': 'vanity=vanity:vanity',
      },
      include_package_data=True,
      keywords='analytics python package index statistics',
      license='GPL',
      long_description=(open('README.rst').read() + '\n' + open(os.path.join(
          'CHANGES.rst')).read()),
      name='vanity',
      py_modules=[
          'vanity',
      ],
      test_suite='tests.TestSuite',
      url='https://github.com/aclark4life/vanity',
      version=VERSION,
      zip_safe=True, )
