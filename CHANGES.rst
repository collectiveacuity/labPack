ChangeLog
=========

0.16 (2018.02.07)
-----------------
* [FEATURE ADDED] requestsHandler class as parent class to handle requests connectivity
* [UPDATE] herokuClient to reflect latest heroku-cli updates to core plugins
* [UPDATE] appdataClient to make absent directories in root_path argument
* [UPDATE] dockerClient synopsis method retrieves port mapping on inactive containers
* [BUG FIX] added recursion through dicts and lists in clean_data method of data package
* [BUG FIX] added shell=True to check_output in dockerClient

0.15 (2018.02.03)
-----------------
* [FEATURE ADDED] findClient class for sending/receiving data from a FIND server
* [FEATURE ADDED] section_text function added to grammar package to partition text strings
* [UPDATE] syncGatewayClient with a public read-only document bucket option
* [BUG FIX] removed lurking keypad_type argument in telegramBotClient

0.14 (2017.12.20)
-----------------
* [BUG FIX] fixed missing init in speech package folder

0.13 (2017.12.12)
-----------------
* [FEATURE ADDED] syncGatewayClient class for storing records in couchbase sync gateway
* [FEATURE ADDED] sqlClient class for handling records stored in SQL databases
* [FEATURE ADDED] ip package added to records to obtain ip address information
* [FEATURE ADDED] pollyClient class for synthesizing speech with AWS Polly API
* [FEATURE ADDED] mapping package of recursive methods to handle nested data
* [FEATURE ADDED] datasets package of tables and methods for accessing the tables
* [UPDATE] root path argument added to appdataClient to override default root path
* [UPDATE] rfc2822 string output added to labDT methods
* [UPDATE] error reporting is improved in validate_request_content method
* [UPDATE] added relative path option for appdataClient root folder

0.12 (2017.07.27)
-----------------
* [FEATURE ADDED] s3Client class for handling record storage on AWS s3
* [FEATURE ADDED] dropboxClient class for handling record storage on Dropbox
* [FEATURE ADDED] driveClient class for handling record storage on Google Drive
* [FEATURE ADDED] comparison package to list differences between two data architectures 
* [FEATURE ADDED] filters package of methods to compile search filters 
* [FEATURE ADDED] encoding package for encoding/decoding record data from ext type
* [TESTS ADDED] test scripts for s3Client, dropboxClient and driveClient
* [REFACTOR] create method changed to save method in appdataClient class
* [REFACTOR] read method changed to load method in appdataClient class
* [UPDATE] body_dict arg replaced with record_data in appdataClient now requires bytes

0.11 (2017.06.30)
-----------------
* [BUG FIX] fixed sshClient init element key name error

0.10 (2017.06.30)
-----------------
* [FEATURE ADDED] sshClient class for handling ssh connections to ec2 instance
* [FEATURE ADDED] ec2Client class for handling aws ec2 interactions
* [FEATURE ADDED] iamClient class for handling aws authentication
* [FEATURE ADDED] ip package for retrieving ip addresses
* [FEATURE ADDED] conversion package for handling data format conversion
* [FEATURE ADDED] grammar package for handling common grammar constructions
* [FEATURE ADDED] documentation pages created on github.io
* [UPDATE] added byte_data argument to appdataClient.create method
* [UPDATE] added validate_extension function to regex package
* [BUG FIX] fixed localhostClient.os.release redeclared as uname().version

0.9 (2017.04.18)
----------------
* [FEATURE ADDED] watsonSpeechClient class for interacting with watson api
* [FEATURE ADDED] mailgunClient class for interacting with mailgun email api
* [FEATURE ADDED] mandrillClient class for interacting with mandrill email api
* [UPDATE] added rfc2822 method to labDT class to output compliant format
* [UPDATE] added remove method to settings package to handle async deletion
* [UPDATE] added jwt session token extraction method to flask parsing package
* [UPDATE] added documentation for installation of libmagic on windows 64 bits
* [BUG FIX] fixed key error on oauth2Client.get_token on failed request
* [BUG FIX] weird feature in flask.Request.args which returns values as lists
* [BUG FIX] error in get_file method of telegramClient class
* [REFACTOR] changed validate_request_details to validate_request_content

0.8 (2016.12.31)
----------------
* [FEATURE ADDED] oauth2Client class for interacting with oauth2 standard APIs
* [FEATURE ADDED] twilioClient class for interacting with twilio messaging api
* [FEATURE ADDED] meetupClient class for interacting with meetup event api
* [UPDATE] apschedulerClient incorporates requests_handler argument
* [UPDATE] retrieve_function incorporates pkgutil module for walking packages
* [UPDATE] __init__ added to all sub-folders for proper package recognition
* [BUG FIX] invalid url error on Request.prepare() method in handle_requests
* [REFACTOR] file_path argument in save_settings function moved to first positional
* [REFACTOR] camelcase methods in localhostClient & appdataClient replaced with underscore

0.7 (2016.11.15)
----------------
* [FEATURE ADDED] handle_requests method added to handler package to handle requests errors
* [FEATURE ADDED] validate_request_details method added to flask package
* [BUG FIX] makedir error for files without path information

0.6 (2016.11.12)
----------------
* [REFACTOR] classes compiler package renamed to objects for future clarity
* [FEATURE ADDED] telegramBotClient class for interacting with telegram bot API **
* [FEATURE ADDED] movesClient class for retrieving user data from moves app API
* [FEATURE ADDED] apschedulerClient class for interacting with a flask apscheduler service
* [FEATURE ADDED] labMagic class for retrieving metadata information about data
* ** telegram client only covers updates, messages and photos

0.5 (2016.11.01)
----------------
* [REFACTOR] Packages have been refactored to lowercase to avoid class syntax
* [FEATURE ADDED] classes compiler package for generating class attributes
* [FEATURE ADDED] flask parsing package for parsing request and response data
* [FEATURE ADDED] settings package for handling local configuration settings
* {WIP] Packages for interaction with moves and telegram api are included

0.4 (2016.10.11)
----------------
* [REFACTOR] All previous methods have been refactored to sub-folders
* [FEATURES ADDED] drep compiler package for encrypted file storage protocol
* [FEATURES ADDED] labCrypt package for encrypted data using AES 256bit sha512
* [FEATURES ADDED] labPerform package for running performance tests
* [FEATURES ADDED] labRegex parsing package for mapping n-grams in strings
* [FEATURES ADDED] appdataClient class for managing file storage on local host
* [FEATURES ADDED] localhostClient class for negotiating os specific methods

0.3 (2016.05.31)
----------------
* [BUG FIX] Missing python-dateutil dependency added to setup

0.2 (2016.05.30)
----------------
* Upload of Module to PyPi
* Creation of GitHub Repo
* Separation of under-development methods from public methods in git

0.1 (2016.03.24)
----------------
* Local Build of Package
* Creation of BitBucket Repo