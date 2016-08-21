Changelog
=========

2.2.2 (2016-08-21)
------------------

- Fix Python 3 JSON issue
  [mattjegan]

2.2.1 (2016-04-27)
------------------

- Add message *** Note: PyPI stats are broken again; we're now waiting for warehouse. https://github.com/aclark4life/vanity/issues/22 ***

2.2.0 (2016-01-06)
------------------

- Add ``--pattern`` option
  [hugovk]

2.1.0 (2015-07-03)
------------------

- Use PyPI JSON API via ``--json``
- Replace print with logging

2.0.4 (2014-09-02)
------------------

- Query /pypi/ instead of /simple/, fixes https://github.com/aclark4life/vanity/issues/12

2.0.3 (2013-05-27)
------------------

- New life: http://mail.python.org/pipermail/distutils-sig/2013-June/021344.html

2.0.2 (2013-05-27)
------------------

- Fix typo

2.0.1 (2013-05-27)
------------------

- End of life: http://mail.python.org/pipermail/distutils-sig/2013-May/020855.html

2.0.0 (2013-05-26)
------------------

- Revert removal of ``--quiet`` option
- Support multi-package entry e.g. ``$ vanity setuptools distribute``

1.2.5 (2013-03-17)
------------------

- Switch to argparse 
- Support query by version spec e.g. ``$ vanity pillow==2.0.0``
- Remove ``--quiet`` option
- Officially add Python 3 support

1.2.4 (2013-02-19)
------------------

- Query PyPI via https
- Return usage statement when no args passed

1.2.3 (2012-08-08)
------------------

- Use optparse for option and argument parsing
  [JNRowe]
- Don't fail when the en_US locale isn't available
  [JNRowe]
- Python 3 compatibility
  [JNRowe]

1.2.2 (2012-07-31)
------------------

- Remove blessings integration which breaks on Windows

1.2.1 (2012-02-15)
------------------

- Make verbose the default
- Add blessings support to make output pretty
- install_requires requests for future refactor
- Enforce available command line options better

1.2.0 (2012-01-30)
------------------

- Add verbose option to display file name, upload date, and download count per release
- Add locale to format downloads e.g. ``700,232 times`` instead of ``700232 times``

1.1.2 (2011-10-28)
------------------

- Fix regression: Re-fix download counts
  [JNRowe]

1.1.1 (2011-10-27)
------------------

- Refactor: create ``downloads_total`` function to make external use simpler
  [kennethreitz]

1.1.0 (2011-10-25)
------------------

- Bug fixes: support for case insensitive project names and support for counting all release files (e.g. binaries in addition to sdist) and correct number of release files
  [JNRowe]

1.0 (04-13-2011)
----------------

- Initial release based on code from `Products.PloneSoftwareCenter`_ by `David Glick`_
                                                                                                                                           
.. _`Products.PloneSoftwareCenter`: https://pypi.python.org/pypi/Products.PloneSoftwareCenter
.. _`David Glick`: http://glicksoftware.com
