__author__ = 'rcj1492'
__created__ = '2015.08'

from timeit import default_timer as timer

from processor.methods.general.labValidation import *
from processor.methods.general.labRandom import *
from processor.methods.general.labData import *
from processor.methods.general.labRecords import *

class labTest(object):

    '''
        a class for reporting the performance of a test on a method
    '''

    def __init__(self, test_method, quiet=False, performance=False):
        method_name = getattr(test_method, '__name__', '??? (try returning method instead of %s)' % test_method.__class__)
        if not quiet:
            print('Testing: ' + method_name)
        if performance:
            t1 = timer()
        outcome = test_method
        if performance:
            t2 = timer()
            print(str(t2 - t1) + ' seconds')

unitList = [
    labValid.unitTests(),
    parseString('').unitTests(),
    labRandom.unitTests(),
    labDecimal(0).unitTests(),
    labBytes('').unitTests(),
    modData({}).unitTests(),
    deltaData({},{}).unitTests(),
    labID().unitTests(),
    labDT.unitTests()
]

performanceList = []

integrationList = []

for item in unitList:
    labTest(item, True)
for item in performanceList:
    labTest(item, True, True)
for item in integrationList:
    labTest(item, True)