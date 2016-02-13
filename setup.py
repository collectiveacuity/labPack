__author__ = 'rcj1492'
__created__ = '2015.11'

from setuptools import setup, find_packages

'''
References:
https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distutils/index.html

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip bdist_wheel

Upload Distributions to PyPi:
twine register dist/*
twine upload dist/*

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files

Old Methods:
python setup.py sdist bdist_wheel upload  # for PyPi
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
'''

setup(
    name="labPack",
    version="0.1.0",
    author = __author__,
    maintainer_email="support@collectiveacuity.com",
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(exclude=['cred','tests','models','notes','oldTools']),  # Needed for bdist
    license="MIT",
    description="A Collection of Methods to Handle Data Collection & Processing",
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonmodel" >= "1.0",
        "selenium" >= "2.51.1",
        "splinter" >= "0.7.3"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)