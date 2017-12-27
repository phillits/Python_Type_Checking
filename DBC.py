'''
Filename: DBC.py
Author: Tyler Phillips

This module contains resources to make designing functions by contract (ie. 
testing inputs and outputs) as efficient and organized as possible.
'''

# Import modules
import inspect
###############################################################################

# Global variables
NUM = (int, float)
###############################################################################

# Exceptions
class OutputError(Exception):
    
    '''
    This exception should be raised when a function tries to return an 
    unacceptable value, whether that's of the wrong type or the right type but 
    the wrong value.
    '''
    
    def __init__(self, error_message: str = ''):
        
        '''
        Parameter:
            error_message: Error message to be displayed when exception is 
                           raised
        '''
        
        # Test inputs
        if not isinstance(error_message, str):
            raise TypeError('OutputError requires str for error_message.')
        
        # Define attributes
        self.error_message = error_message # Error message displayed (str)
        
        Exception.__init__(self, self.error_message)
###############################################################################

# Classes

###############################################################################

# Functions
def check_arg_type(parameter, parameter_name, acceptable_types):
    
    '''
    Purpose:              This function is equivalent to 
                          assert isinstance(parameter, acceptable_types), but 
                          it writes an error message automatically and raises 
                          an ArgumentError instead of an AssertionError.  It is
                          intended to be used for checking that arguments given
                          to a function are of an acceptable type.  
    Parameters:
        parameter:        Parameter to be checked
        parameter_name:   The name of the parameter to be checked as a str
        acceptable_types: A single type or a tuple of types
    Returns:              None.
    
    Example error statement: function_name requires int or float for 
                             parameter_name.
    '''
    
    # Test input
    if not isinstance(parameter_name, str):
        raise TypeError('check_arg_type requires str for parameter_name.')
    if not isinstance(acceptable_types, (type, tuple)):
        raise TypeError('check_arg_type requires type or tuple for '
                        'acceptable_types.')
    if isinstance(acceptable_types, tuple):
        for item in acceptable_types:
            if not isinstance(item, type):
                raise TypeError('All items in acceptable_types must be types.')
    
    # Define variables
    function_name = inspect.stack()[1][3] # Name of func that called this one
    
    if not isinstance(parameter, acceptable_types):
        raise ArgumentError(function_name, parameter_name, acceptable_types)
    
    # Return
    return None

def check_output_type(variable, acceptable_types):
    
    '''
    Purpose:              This function should be used to test the type of a 
                          variable before it is returned from a function.  If 
                          the variable is not of an acceptable type, it will 
                          raise an OutputError.
    Parameters:
        variable:         Variable to be checked
        acceptable_types: A single type or a tuple of types
    Returns:              None
    '''

    # Test inputs
    if not isinstance(acceptable_types, (type, tuple)):
        raise TypeError('check_output_type requires type or tuple for '
                        'acceptable_types.')
    if isinstance(acceptable_types, tuple):
        for item in acceptable_types:
            if not isinstance(item, type):
                raise TypeError('All items in acceptable_types must be types.')
    
    # Define variables
    function_name = inspect.stack()[1][3] # Name of func that called this one
    
    # Create error message
    # One acceptable type
    if isinstance(acceptable_types, type):
        error_message = (function_name + ' should return ' + 
                         acceptable_types.__name__ + '.')
    # Two acceptable types
    elif len(acceptable_types) == 2:
        error_message = (function_name + ' should return ' + 
                         acceptable_types[0].__name__ + ' or ' + 
                         acceptable_types[1].__name__ + '.')
    # Three or more acceptable types
    else:
        type_names = ''
        for item in acceptable_types[:-1]:
            type_names += item.__name__ + ', '
        type_names += 'or ' + acceptable_types[-1].__name__
        error_message = (function_name + ' should return ' + type_names + '.')
    
    if not isinstance(variable, acceptable_types):
        raise OutputError(error_message)
    
    # Return
    return None

def check_output_type(output_value) -> type(None):
    
    '''
    Purpose: 
    
    Checks a value which is intended to be returned against the acceptable 
    type(s) specified by the function's annotation for the return value.  
    Annotation can be a type or a tuple containing multiple types.  If the 
    annotation is of any other form or if there is no annotation, the function 
    will do nothing.  If the value given is not of an acceptable type, an 
    OutputError will be raised.
    
    Parameter:
        output_value: The value intended to be returned.  This is the value 
                      whose type will be checked.
    Returns:          None.
    
    Format of error message of OutputError if check fails:
    
        "<function> should return <type>."
        
        or 
        
        "<function> should return <type1>, <type2>, ... or <type3>."
    '''
    
    function = code.get_function()
    try:
        acceptable_types = function.__annotations__['return']
    except KeyError:
        return None
    if not isinstance(acceptable_types, (type, tuple)):
        return None
    if isinstance(acceptable_types, tuple):
        for item in acceptable_types:
            if not isinstance(type):
                return None
    if not isinstance(output_value, acceptable_types):
        error_message = output_error_message(function.__name__, )
        raise OutputError()

def check_all_argument_types(level: int = 1) -> type(None):
    
    '''
    Purpose:
    
    This function allows for very easy testing of argument types by taking 
    advantage of Python's function annotation feature.  For every parameter 
    whose annotation is either a type or a tuple containing only types, it will
    check the argument passed to the function against those types.  If they 
    don't match, it will raise a TypeError.  Parameters with no annotation or 
    with any other form of annotation will be passed over.
    
    Parameter:
        level: Indicates the level (index in the stack) to check.  0 will check 
               the check_all_argument_types function itself.  1 (the default 
               value) will check the function that called the 
               check_all_argument_types function.  2 will check the function 
               that called that one, and so on.
    Returns:   None.
    
    Format of error message of TypeError if check fails:
    
        "<function> requires <type> for <parameter>."
    
        or
    
        "<function> requires <type1>, <type2>, ... or <type3> for <parameter>."
    '''
    
    # Test input
    if not isinstance(level, int):
        raise TypeError('check_all_argument_types requires int for level.')
    if not level >= 0:
        raise ValueError('level must be >= 0.')
    
    # Define variables
    function = inspect.stack()[level][3]
    