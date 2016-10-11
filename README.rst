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
* **labID**: A class of methods for uniquely identifying records
* **labDT**: A class of methods for transforming datetime data
* **labRandom**: A package of methods for generating random data
* **labPerform**: A package of methods for running performance tests
* **drep**: A file storage protocol for encrypted record data
* **labCrypt**: A package for encrypting/decrypting data using AES256 sha512
* **labRegex**: A class of methods for matching regex patterns
* **appdataClient**: A class of methods for managing file storage in home dir
* **localhostClient**: A class of methods for negotiating OS specific configuration

Features
--------
- Unique IDs which do not conflict nor leak record origin
- Transformations of datetime data between popular formats
- Randomization using best current algorithms
- [FEATURES ADDED] drep compiler package for encrypted file storage protocol
- [FEATURES ADDED] labCrypt package for encrypted data using AES 256bit sha512
- [FEATURES ADDED] labPerform package for running performance tests
- [FEATURES ADDED] labRegex parsing package for mapping n-grams in strings
- [FEATURES ADDED] appdataClient class for managing file storage on local host
- [FEATURES ADDED] localhostClient class for negotiating os specific methods

============
Installation
============
From PyPi::

    $ pip install labpack

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