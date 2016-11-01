import re
from setuptools import setup, find_packages

'''
References:
https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distributing/index.html#distributing-index
https://github.com/jgehrcke/python-cmdline-bootstrap
http://www.pyinstaller.org/

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip
pip wheel --no-index --no-deps --wheel-dir dist dist/labpack-0.5.tar.gz

Upload Distributions to PyPi:
python setup.py register
twine upload dist/[module-version]*

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link
# remove command line tool in ../Python/Python35-32/Scripts/

CLI Installation:
command = 'name of command'
module = 'name of module'
    entry_points = {
        "console_scripts": ['%s = %s.cli:cli' % (command, module)]
    },

System Installation:
# http://www.pyinstaller.org/

Git Public Setup:
https://stackoverflow.com/questions/37422221/git-remove-a-file-from-a-branch-keep-it-in-the-master/37422311
git remote add github https://github.com/...
git branch public
git checkout public
git rm --cached --ignore-unmatch -r dev/*
git rm --cached --ignore-unmatch -r tests_dev/*
git rm --cached --ignore-unmatch -r notes/*
git commit -m 'removed dev files before public push'
git push github public
git checkout -f master

Git Public Updates:
git checkout public
git merge master
git push github public
git checkout -f master
'''

config_file = open('labpack/__init__.py').read()
version = re.search("^__version__\s*=\s*'(.*)'", config_file, re.M).group(1)
# command = re.search("^__command__\s*=\s*'(.*)'", config_file, re.M).group(1)
license_terms = re.search("^__license__\s*=\s*'(.*)'", config_file, re.M).group(1)
module = re.search("^__module__\s*=\s*'(.*)'", config_file, re.M).group(1)
author = re.search("^__author__\s*=\s*'(.*)'", config_file, re.M).group(1)
email = re.search("^__email__\s*=\s*'(.*)'", config_file, re.M).group(1)
url = re.search("^__url__\s*=\s*'(.*)'", config_file, re.M).group(1)
# author_list = re.search("^__authors__\s*=\s*'(.*)'", config_file, re.M).group(1)

setup(
    name=module,
    version=version,
    author=author,
    author_email=email,
    maintainer_email=email,
    url=url,
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(),  # exclude=['cred','data','keys','dev','docs','tests','tests_dev','models','notes','tinkering'] Needed for bdist
    license=license_terms,
    description="A Collection of Methods for Data Collection & Processing",
    long_description=open('README.rst').read(),
    install_requires=[
        'pytz>=2015.7',
        'tzlocal>=1.2',
        'python-dateutil>=2.4.2',
        'pyyaml>=3.12',
        'jsonmodel',
        'requests'
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