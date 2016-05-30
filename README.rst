.. image:: https://img.shields.io/pypi/v/labpack.svg
    :target: https://pypi.python.org/pypi/labpack
.. image:: https://img.shields.io/pypi/dm/labpack.svg
    :target: https://pypi.python.org/pypi/labpack
.. image:: https://img.shields.io/pypi/l/labpack.svg
    :target: https://pypi.python.org/pypi/labpack

=======
labPack
=======
*A Collection of Methods for Data Collection & Processing*

:Downloads: http://pypi.python.org/pypi/labPack
:Source: https://github.com/collectiveacuity/labPack

Top-Level Classes
-----------------
* **labID**: A class of methods for uniquely identifying objects
* **labDT**: A class of methods for transforming datetime data
* **labRandom**: A class of methods for generating random data

Features
--------
- Unique IDs which do not conflict nor leak record origin
- Transformations of datetime data between popular formats
- Randomization using best current algorithms

============
Installation
============
From PyPi::

    $
    $ python setup.py install

From GitHub::

    $ git clone https://github.com/collectiveacuity/labPack
    $ cd labPack
    $ python setup.py install

Getting Started
---------------
This module is designed to make the process of retrieving, managing and processing data more uniform across a variety of different sources and structures. A number of module methods are implementations of built-in python packages and standard python imports which have been optimized for data management and compensate for the messy state of real data. The methods in this module aggregate and curate python resources and online APIs to provide a set of best practices for handling data.

Create an unique ID for records::

    from labpack.records import labID

    id = labID()
    url_safe_id_string = id.id48
    id_datetime = id.epoch

For more details about how to use labPack, refer to the
`Reference Documentation on GitHub
<https://github.com/collectiveacuity/labPack/blob/public/REFERENCE.rst>`_