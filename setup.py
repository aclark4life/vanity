
from setuptools import setup
import os

setup(
    name='vanity',
    version='1.1.1',
    description='Easy access to PyPI download stats',
    long_description=(
        open('README.rst').read() +
        open(os.path.join('docs', 'HISTORY.txt')).read()),
    py_modules=['vanity'],
    author = 'Alex Clark',
    author_email = 'Alex Clark',
    url='https://github.com/aclark4life/vanity',
    entry_points = """
    [console_scripts]
    vanity = vanity:main
    """
)
