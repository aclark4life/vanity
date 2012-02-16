
Introduction
============

Easy access to download statistics from the Python Package Index, via the command line::

    $ vanity django
    Django-1.1.3.tar.gz     2010-12-23    2,643
    Django-1.1.4.tar.gz     2011-02-09    4,629
      Django-1.2.tar.gz     2010-05-17   16,148
    Django-1.2.1.tar.gz     2010-05-24   65,379
    Django-1.2.2.tar.gz     2010-09-09    2,482
    Django-1.2.3.tar.gz     2010-09-11   74,277
    Django-1.2.4.tar.gz     2010-12-23   50,307
    Django-1.2.5.tar.gz     2011-02-09   64,545
    Django-1.2.6.tar.gz     2011-09-10      470
    Django-1.2.7.tar.gz     2011-09-11    7,291
      Django-1.3.tar.gz     2011-03-23  246,589
    Django-1.3.1.tar.gz     2011-09-10  207,103
    -------------------------------------------
    Django has been downloaded 741,863 times!


Installation
============

Install via::

    $ pip install vanity

Or::

    $ easy_install vanity

Or download the compressed archive, extract it, and inside it run::

    $ python setup.py install

Advanced options
================

To supress the display of **file name**, **upload date**, and **download count** for each release,
specify quite mode with ``-q`` or ``--quiet``::

    $ vanity django -q
    Django has been downloaded 741,863 times!

Credits
=======

- Based on code from `Products.PloneSoftwareCenter`_ written by
  `David Glick`_.

.. _`Products.PloneSoftwareCenter`: http://pypi.python.org/pypi/Products.PloneSoftwareCenter
.. _`David Glick`: http://davisagli.com
