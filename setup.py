__author__ = 'rcj1492'
__created__ = '2015.11'

from setuptools import setup, find_packages

# For more examples, see
#   https://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest/creation.html

setup(
   name="oldTools",
   version="0.1.0",
   author = __author__,
   include_package_data=True,  # Checks MANIFEST.in for explicit rules
   packages = find_packages(),
   license="LICENSE.txt",
   description="A Collection of Classes for Handling Data Collection & Processing",
   long_description=open('README.rst').read(),
   install_requires=[
      "paramiko >= 1.15.2",
      "pytz" >= "2015.2",
      "scp" >= "0.10.2",
      "boto3" >= "1.1.4",
      "pytest" >= "2.7.2",
      "selenium" >= "2.51.1"
   ],
   classifiers=[
      'Development Status :: Alpha',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.4'
   ]
)