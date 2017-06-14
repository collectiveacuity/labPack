__author__ = 'rcj1492'
__created__ = '2016.02'

class AWSConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to AWS website with %s request.' % message
        super(AWSConnectionError, self).__init__(text)
        self.errors = errors