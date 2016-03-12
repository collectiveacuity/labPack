__author__ = 'rcj1492'
__created__ = '2016.01'

'''
https://stackoverflow.com/questions/27083599/how-to-execute-decorated-class-methods-stored-in-a-list-object/
'''

import types

class Bar(object):

    def __init__(self):
        self.message = "I'm %s" % (self.__class__.__name__)

    def example_01(self):
       print(self.message)
       print("Executing example_01")

    def example_02(self):
        print(self.message)
        print("Executing example_02")

examples = list()
testBar = Bar()
methods = Bar.__dict__
for k, v in methods.items():
    if isinstance(v, types.FunctionType):
        if k != '__init__':
            examples.append(testBar.__getattribute__(k))

def main():
    for method in examples:
        method()

if __name__ == '__main__':
    main()