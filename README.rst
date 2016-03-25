.. image:: https://img.shields.io/pypi/v/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel
.. image:: https://img.shields.io/pypi/dm/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel
.. image:: https://img.shields.io/pypi/l/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel

=======
labPack
=======
*A Collection of Methods for Data Collection & Processing*

:Downloads: http://pypi.python.org/pypi/labPack
:Source: https://github.com/collectiveacuity/labPack

Top-Level Classes
-----------------
* **labID**: A class of methods for uniquely identifying objects
* **labString**: A class of methods for parsing, formatting and validating a string
* **labRandom**: A class of methods for generating random data

Features
--------
*

============
Installation
============
From PyPi::

    $ pip install labPack

From GitHub::

    $ git clone https://github.com/collectiveacuity/labPack
    $ python setup.py install

Getting Started
---------------
This module is designed to manage...

Run a string validation tool::

    from labPack.validations import labString

    greeting = labString('hi').rename('mom')

For more details about how to use labPack, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/labpack/src/master/REFERENCE.rst>`_