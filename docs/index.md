# Lab Pack
_A Collection of Methods for Data Collection & Processing_  
by [Collective Acuity](http://collectiveacuity.com)

<table>
  <tbody>
    <tr>
      <td><b>Downloads</b></td>
      <td><a href="http://pypi.python.org/pypi/labpack">http://pypi.python.org/pypi/labPack</a></td>
    </tr>
    <tr>
      <td><b>Source</b></td>
      <td><a href="https://github.com/collectiveacuity/labpack">https://github.com/collectiveacuity/labPack</a></td>
    </tr>
    <tr>
      <td><b>Documentation</b></td>
      <td><a href="https://collectiveacuity.github.io/labPack">https://collectiveacuity.github.io/labPack/</a></td>
    </tr>
  </tbody>
</table>

## Introduction
Lab Pack is designed to make the process of retrieving, managing and processing data more uniform across a variety of different sources and structures. The classes and methods in this module aggregate and curate python resources and online APIs to provide a set of best practices for handling data across laboratory projects.

## Installation
From PyPi
```bash
    $ pip install labpack
```
From GitHub
```bash
    $ git clone https://github.com/collectiveacuity/labpack
    $ cd labpack
    $ python setup.py install
```

## Getting Started
This module contains a variety of classes, clients and packages for use in laboratory projects. For example to store records in an indexed file store on the local device, you can use the following methods:

Create an unique ID for records::

    from labpack.records.id import labID

    id = labID()
    url_safe_id_string = id.id48
    id_datetime = id.epoch
    id_mac_address = id.mac

Save record data in local user data::

    from labpack.storage.appdata import appdataClient

    msg_key = '%s/%s.yaml' % (id_mac_address, id_datetime)
    msg_details = { 'dt': id_datetime, 'mac': id_mac_address, 'msg': 'Text me back' }
    msg_client = appdataClient('Outgoing', 'My Team', 'My App')
    mgs_client.create(msg_key, msg_details)

## Further Reading
For a list of the methods in this module, refer to the [Classes](classes.md), [Clients](clients.md) and [Packages](packages.md) pages.