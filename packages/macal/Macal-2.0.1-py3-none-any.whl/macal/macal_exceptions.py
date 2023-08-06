#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_exceptions.py                                                           #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Exceptions                                                                            #
#                                                                                                 #
###################################################################################################

"""Exceptions classes for macal 2.0"""

from .macal_scope import PScope

class InvalidFunctionCallException(Exception):
    def __init__(self, name: str, funcname: str, scope: PScope):
        self.Name = name
        self.Scope = scope
        self.FuncName = funcname

    def __str__(self):
        return f"Invalid function call: {self.Name}, expected {self.FuncName}. {self.Scope}";

class InvalidParamCountException(Exception):
    def __init__(self, name: str, scope: PScope, length: int, required: int):
        self.Name = name
        self.Scope = scope
        self.Length = length
        self.Required = required

    def __str__(self):
        return f"{self.Name}: Invalid number of parameters provided: {self.Length}, required: {self.Required}. ({self.Scope})"

class MissingParameterException(Exception):
    def __init__(self, name: str, scope: PScope, param_name: str):
        self.Name = name
        self.Scope = scope
        self.ParamName = param_name
        
    def __str__(self):
        return f"{self.Name}: Function parameter missing: {self.ParamName}. ({self.Scope})"

class InvalidParamTypeException(Exception):
    def __init__(self, name: str, scope: PScope, param_name: str, invalid_type: str, required_type: str):
        self.Name = name
        self.Scope = scope
        self.ParamName = param_name
        self.InvalidType = invalid_type
        self.RequiredType = required_type
        
    def __str__(self):
        return f"{self.Name}: Invalid parameter ({self.ParamName}) type: {self.InvalidType}, required: {self.RequiredType}. ({self.Scope})"

class VariableNotFoundException(Exception):
    def __init__(self, name: str, scope: PScope):
        self.Name = name
        self.Scope = scope
        
    def __str__(self):
        return f"Exception: Variable not found ({self.Name}). ({self.Scope})"

class InvalidVariableTypeException(Exception):
    def __init__(self, name: str, scope: PScope, invalid_type: str, required_type: str):
        self.Name = name
        self.Scope = scope
        self.InvalidType = invalid_type
        self.RequiredType = required_type
        
    def __str__(self):
        return f"Exception: Invalid variable ({self.Name}) type: {self.InvalidType}, required: {self.RequiredType}. ({self.Scope})"

class RuntimeError(Exception):
    def __init__(self, message: str):
        self.Message = message
        
    def __str__(self):
        return f"Runtime Error: {self.Message}"