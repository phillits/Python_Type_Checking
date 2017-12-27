'''
Filename: DBC_test.py
Author: Tyler Phillips

Test program for DBC module
'''

from DBC import *
import unit_testing as ut

# Class tests
class TestArgumentError(ut.ClassTest):
    
    def __init__(self):
        
        ut.ClassTest.__init__(self)
    
    def test___init__(self):
        
        ut.test(isinstance(ArgumentError('function', 'parameter', tuple), 
                        ArgumentError))
        
        argumenterror1 = ArgumentError('test', 'expression', bool)
        ut.test(argumenterror1.function_name == 'test')
        ut.test(argumenterror1.parameter_name == 'expression')
        ut.test(argumenterror1.acceptable_types == bool)
        ut.test(argumenterror1.error_message == ('test requires bool for '
                                              'expression.'))
    
argumenterror = TestArgumentError()

class TestOutputError(ut.ClassTest):
    
    def __init__(self):
        
        ut.ClassTest.__init__(self)
    
    def test___init__(self):
        
        ut.test(isinstance(OutputError('hi'), OutputError))
        
        outputerror1 = OutputError('Function should return int.')
        ut.test(outputerror1.error_message == 'Function should return int.')

outputerror = TestOutputError()

# Function tests
def test_check_arg_type():
    
    ut.test(check_arg_type(1, 'num', (int, float)) == None)
    ut.test(check_arg_type('', 'string', str) == None)
    ut.test(check_arg_type([], 'data', (str, int, list, tuple)) == None)
    
    errors = 0
    try:
        ut.test(check_arg_type(1, 'string', str) == None)
    except ArgumentError:
        errors += 1
    try:
        ut.test(check_arg_type('', 'num', (int, float)) == None)
    except ArgumentError:
        errors += 1
    try:
        ut.test(check_arg_type(1.5, 'parameter', (int, str, tuple, list, bool))
                == None)
    except ArgumentError:
        errors += 1
    ut.test(errors == 3)

def test_check_output_type():
    
    ut.test(check_output_type(5, int) == None)
    ut.test(check_output_type('', str) == None)
    ut.test(check_output_type('', (list, str, int)) == None)
    
    errors = 0
    try:
        ut.test(check_output_type('', int) == None)
    except OutputError:
        errors += 1
    try:
        ut.test(check_output_type('', list) == None)
    except OutputError:
        errors += 1
    try:
        ut.test(check_output_type(8.7, (list, str, tuple)) == None)
    except OutputError:
        errors += 1
    ut.test(errors == 3)

def main():
    
    # Class tests
    argumenterror.test_all()
    outputerror.test_all()
    
    # Function tests
    test_check_arg_type()
    test_check_output_type()
    
    print('All tests passed.')

if __name__ == '__main__':
    main()