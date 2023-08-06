#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_system.py                                                       #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Strings Library                                                                       #
#                                                                                                 #
###################################################################################################

"""Strings library implementation"""

from .macal_library import PLibrary
from .macal_variable_types import ANY, INT, STRING
from .macal_parsernodetypes import VARIABLE
from .macal_interpreterconsts import FuncArg
from .macal_scope import PScope
from .macal_function import PFunction

from .macal_exceptions import InvalidVariableTypeException

class LibraryStrings(PLibrary):
    def __init__(self):
        super().__init__("strings")
        self.RegisterFunction("len",      [FuncArg("arg", ANY)], self.StrLen)
        self.RegisterFunction("left",     [FuncArg("arg", STRING),    FuncArg("length", INT)], self.StrLeft)
        self.RegisterFunction("mid",      [FuncArg("arg", STRING),    FuncArg("start", INT),   FuncArg("length", INT)], self.StrMid)
        self.RegisterFunction("tostring", [FuncArg("arg", ANY)], self.ToString)
        self.RegisterFunction("format",   [FuncArg("format", STRING), FuncArg("arg", ANY)], self.StrFormat)
        self.RegisterFunction("replace",  [FuncArg("var", VARIABLE),  FuncArg("from", STRING), FuncArg("with", STRING)], self.StrReplace)

    def StrLen(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        result = len(self.GetParamValue(params, "arg"))
        scope.SetReturnValue(result, INT)
    
    def StrLeft(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of left function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        result = self.GetParamValue(params, "arg")[0:self.GetParamValue(params, "length")]
        scope.SetReturnValue(result, STRING)

    def StrMid(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of mid function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        result = self.GetParamValue(params, "arg")[self.GetParamValue(params, "start"):self.GetParamValue(params, "length")]
        scope.SetReturnValue(result, STRING);

    def ToString(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        argvalue = self.GetParamValue(params, "arg")
        result = f"{argvalue}"
        scope.SetReturnValue(result, STRING);

    def StrFormat(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        result = self.GetParamValue(params, "format").format(self.GetParamValue(params, "arg"))
        scope.SetReturnValue(result, STRING);

    def StrReplace(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.parameters)
        var = self.GetVariableFromParam(params, scope, "var")
        if var.get_type() != STRING:
            InvalidVariableTypeException(var.name, scope, var.get_type(), STRING);
        result = var.get_value().replace(self.GetParamValue(params, "from"), self.GetParamValue(params, "with"))
        var.set_value(result)
        scope.SetReturnValue(result, STRING);
