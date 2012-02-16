from setuptools import setup
import os

setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    description='Easy access to PyPI download stats',
    entry_points={
        'console_scripts': 'vanity = vanity:main'
    },
    include_package_data=True,
    install_requires=[
        'blessings',
        'requests',
    ],
    long_description=(open('README.rst').read() + open(
        os.path.join('docs', 'HISTORY.txt')).read()),
    maintainer='pythonpackages',
    maintainer_email='info@pythonpackages.com',
    name='vanity',
    py_modules=[
        'vanity'
    ],
    url='https://github.com/aclark4life/vanity',
    version='1.2.1',
)
