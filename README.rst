
Introduction
============

Easy access to PyPI download stats via command line::

    $ vanity django
    Package `Django` has been downloaded 700,232 times!


Installation
============

Install via::

    $ pip install vanity

Or::

    $ easy_install vanity

Or download the compressed archive, extract it, and inside it run::

    $ python setup.py install

Advanced
========

To display **file name**, **upload date**, and **download count** for each release,
specify verbose mode with ``-v`` or ``--verbose``::

    $ vanity django -v
    Django-1.1.3.tar.gz     2010-12-23    2,618
    Django-1.1.4.tar.gz     2011-02-09    4,476
      Django-1.2.tar.gz     2010-05-17   15,876
    Django-1.2.1.tar.gz     2010-05-24   65,120
    Django-1.2.2.tar.gz     2010-09-09    2,467
    Django-1.2.3.tar.gz     2010-09-11   73,984
    Django-1.2.4.tar.gz     2010-12-23   49,904
    Django-1.2.5.tar.gz     2011-02-09   63,977
    Django-1.2.6.tar.gz     2011-09-10      427
    Django-1.2.7.tar.gz     2011-09-11    6,825
      Django-1.3.tar.gz     2011-03-23  238,504
    Django-1.3.1.tar.gz     2011-09-10  176,054
    -------------------------------------------
    Package `Django` has been downloaded 700,232 times!

Credits
=======

- Based on code from `Products.PloneSoftwareCenter`_ written by
  `David Glick`_.

.. _`Products.PloneSoftwareCenter`: http://pypi.python.org/pypi/Products.PloneSoftwareCenter
.. _`David Glick`: http://davisagli.com
