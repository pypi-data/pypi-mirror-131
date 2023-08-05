#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library.py                                                              #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Library class                                                                         #
#                                                                                                 #
###################################################################################################

"""Base class for macal Library"""

from .macal_lextoken import Token, Location
from .macal_lextokentypes import LPAREN
from .macal_variable_types import ANY, PARAMS
from .macal_parsernodes import ast_Block, ast_Variable, ast_function_Param_list
from .macal_function import PFunction
from .macal_scope import PScope
from .macal_utilities import ListItemByName
from .macal_exceptions import (InvalidFunctionCallException, InvalidParamCountException, 
                              MissingParameterException, InvalidParamTypeException,
                              VariableNotFoundException)

LIB_LOC = Location(-1, -1, -1)

class PLibrary:
    """Base class for Libraries"""
    def __init__(self, name):
        self.name:      str             = name
        self.functions: list[PFunction] = []
        self.version:   str             = "2.0"

    def CreateParam(self, name: str, param_type: str):
        """Create a new parameter for the function"""
        return ast_Variable(Token(param_type, name, LIB_LOC))

    def RegisterFunction(self, name: str, params: list, call_func):
        """Register a new function with the library."""
        prms = ast_function_Param_list(Token(LPAREN, '(', LIB_LOC))
        for param in params:
            prms.params.append(self.CreateParam(param.value, param.item_type))
        fun = PFunction(name, prms, ast_Block(None))
        fun.is_extern = True
        fun.call_extern = call_func
        self.functions.append(fun)

    def ValidateFunction(self, name: str, fn: PFunction):
        """Validate if the function exists."""
        if name != fn.name:
            raise InvalidFunctionCallException(name, fn, scope)
        return True

    def ValidateParams(self, name: str, params: list, scope: PScope, funcparams: list):
        """Validate if all the parameters that where passed are correct."""
        if len(params) != len(funcparams.params):
            raise InvalidParamCountException(name, scope, len(params), len(funcparams))
        for funcparam in funcparams.params:
            param = ListItemByName(params, funcparam.token.value)
            if param is None:
                raise MissingParameterException(name, scope, funcparam.token.value)
            pt = param.get_type()
            if pt != funcparam.token.type and funcparam.token.type != ANY and funcparam.token.type != PARAMS:
                raise InvalidParamTypeException(name, scope, funcparam.token.value, pt, funcparam.token.type);
        return True

    def GetParamValue(self, params: list, name: str):
        """Get the value from a parameter in the params list."""
        param = ListItemByName(params, name)
        if param is None:
            raise MissingParameterException(self.name, None, name)
        return param.get_value()

    def GetVariableFromParam(self, params: list, scope: PScope, name: str):
        """Get a scope variable from a parameter on the parameters list."""
        varname = self.GetParamValue(params, name)
        var = scope.find_variable(varname)
        if var is None:
            raise VariableNotFoundException(varname, scope)
        return var

    def GetFunction(self, name: str):
        """Find function by name"""
        return next((x for x in self.functions if x.name == name), None)
