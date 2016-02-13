__author__ = 'rcj1492'
__created__ = '2015'

# A collection of basic functions in Python

# STRINGS

# create a string
testString = 'test'

# add to a string
testString += 'ing'

# truncate a string
testString = testString[0:4]

# alternative way to add to a string
testString = testString + 'ing'

# print out text
print('testing')

# print out a variable
print(testString)

# print out a string with a variable inside it
print('%s 1, 2, 3.' % testString)

# print out a string with multiple variables inside it
print('%s 1, 2, 3. %s 1, 2, 3.' % (testString, testString))

# replace characters in a string
testString = testString.replace('estin', 'a')

# test that a condition is true
assert testString == 'tag'

# find the start of a the first series of characters in a string (returns an integer)
seriesStart = testString.find('a')

# find the length of a string (returns an integer)
seriesLength = len('a')

# add integers together
seriesEnd = seriesStart + seriesLength

# alternative way to replace a series of characters in a string
testString = testString[0:seriesStart] + 'estin' + testString[seriesEnd:]
assert testString == 'testing'


# DICTIONARIES

# create a dictionary
testDict = {}

# populate a dictionary with a key-value pair
testDict['testKey'] = 'testValue'

# create a dictionary with key-value pairs inside it
copyDict = { 'testKey': 'testValue' }

# find the value of a key in a dictionary
testValue = testDict['testKey']
assert testValue == 'testValue'
assert testDict['testKey'] == copyDict['testKey']

# find a list of the names of keys in a dictionary
keyList = testDict.keys()

# test the existence of a key in a dictionary
if 'testKey' in testDict.keys():
    testValue = testDict['testKey']
assert testValue == 'testValue'

# change the value of a key in a dictionary
testDict['testKey'] = 'newValue'

# remove a key-value pair from a dictionary
del testDict['testKey']


# LISTS

# create a list
testList = []

# populate the end of the list
testList.append('testItem')

# find an item in a list from its location (the first item in a list is always 0)
testItem = testList[0]

# add an entry to the first position in a list
testList.insert(0, 'earlierItem')
assert testList[0] == 'earlierItem'

# find the location of an item in a list
testList.index('earlierItem')

# remove an item from a list based upon its location
del testList[0]

# create a list of primitives from each character in a string
testList = list(testString)
assert testList == ['t', 'e', 's', 't', 'i', 'n', 'g']

# sort a list of primitives by the alpha(or numeric) order of its strings
testList.sort()
assert testList == ['e', 'g', 'i', 'n', 's', 't', 't']

# create a set of unique items
testSet = set(testList)
assert testSet == { 'e', 'g', 'i', 'n', 's', 't' }

# create a list of dictionaries
testList = [ { 'num': 3 }, { 'num': 2 }, { 'num': 1 } ]
assert testList[0]['num'] == 3

# sort a list of dictionaries by the alpha(or numeric) order of a key value
testList = sorted(testList, key=lambda k: k['num'])
assert testList[0]['num'] == 1

# lambda functions are one statement functions that can be treated like values
l = [ [1,0], [2,1], [3,2], [4,1], [5,2], [6,0] ]
arg = { 'key': lambda i: i[1] }
l = sorted(l, **arg)


# CLASSES (of Objects)

# define a string object
testObject = ''

# discover the class of an object
dataType = testObject.__class__

# test if an object is a specific class
if isinstance(testObject, dataType):
    print('testObject is a %s' % dataType)


# ITERATION

# WHILE statements: iterate a process while a condition holds
truthTest = False
counter = 0
while not truthTest:
    counter += 1
    if counter >= 10:
        truthTest = True

# RANGE statements: iterate a process a fixed number of times
testList = []
for num in range(0,10):
    testList.append(num)
assert testList == [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]

# DICTIONARY key-pairs: iterate over all keys in level of dictionary
testDict = { 'testKey': 'testValue' }
for key, value in testDict.items():
    assert key == 'testKey'
    assert value == 'testValue'


# CONDITIONALS

# if, else, elif
# sleep


# FUNCTIONS

# DYNAMIC KEYWORDS: adding dynamic keywords into arguments
# https://stackoverflow.com/questions/337688/dynamic-keyword-arguments-in-python
test_key = 'keyName'
test_value = 'valueString'
kw_args = { test_key: test_value }
def example(**kwargs):
    for key in kwargs.keys():
        return key + ': ' + kwargs[key]
assert example(keyName='valueString') == example(**kw_args)


# EXCEPTIONS & EXCEPTION HANDLING

# test error occurs
import pytest
with pytest.raises(TypeError):
    1 + '1'

# perform an action if an error occurs
try:
    1 + '1'
except TypeError:
    assert True





