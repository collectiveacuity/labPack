=======
labPack
=======
*A Collection of Methods to Handle Data Collection & Processing*

:Source: https://bitbucket.org/collectiveacuity/labpack.git

Top-Level Classes
-----------------
- **labSpeech**: A class to manage the speech-to-text and text-to-speech APIs

Low-Level Classes
-----------------
- **labValidation**: a collection of input tests for the arguments in other labPack methods
- **labTests**: a collection of test classes for testing other labPack methods

AWS Rules & Limits
------------------
* **aws-rules.json**: a json file with the rules and limitations for resource values on AWS

Class Object Models (in models/)
--------------------------------
-

Features
--------
-

Installation
============
From BitBucket::

    $ git clone https://bitbucket.org/collectiveacuity/labpack.git
    $ python setup.py sdist --format=gztar
    $ python setup.py develop  # for local on-the-fly file updates

Getting Started
^^^^^^^^^^^^^^^
This module is designed to manage...

Run a string validation tool::
.. code-block:: python

    from labpack.validators import labString

    greeting = labString('hi').rename('mom')

For more details about how to use labPack, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/labpack/REFERENCE.rst>`_