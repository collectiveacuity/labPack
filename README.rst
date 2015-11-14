========
labTools
========
*A Collection of Classes & REST APIs to Handle Data Collection & Processing*

:Source: https://bitbucket.org/collectiveacuity/labtools.git

Top-Level Classes
-----------------
- **labSpeech**: A class to manage the speech-to-text and text-to-speech APIs

Low-Level Classes
-----------------
- **labValidation**: a collection of input tests for the arguments in other labTools methods
- **labTests**: a collection of test classes for testing other labTools methods

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

    $ pip install git+https://bitbucket.org/collectiveacuity/labtools.git


Getting Started
^^^^^^^^^^^^^^^
This module is designed to manage...

Run the sequence of class unit tests::
.. code-block:: python

    from labTools.labTests import *

    fullTest = unitTests().run()

For more details about how to use labTools, refer to the
`Setup Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/labtools/SETUP.rst>`_