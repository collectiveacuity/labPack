===========
labPack_dev
===========
*A WIP Collection of Methods & APIs to Handle Data Collection & Processing*

:Source: https://bitbucket.org/collectiveacuity/labpack_dev.git

Top-Level Classes
-----------------
- **labScrape**: A class to scrape data from websites
- **labSpeech**: A class to manage the speech-to-text and text-to-speech APIs

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

    from labPack_dev.shorteners import bitlyAPI
    from cred.credentialsBitly import bitlyCredentials

    bitlySession = bitlyAPI(bitlyCredentials)
    bitlySession.shorten('https://mylongdomainname.com/?param=verylongquerystring')

For more details about how to use labPack, refer to the
`Reference Documentation on BitBucket
<https://bitbucket.org/collectiveacuity/labpack_dev/src/master/REFERENCE.rst>`_