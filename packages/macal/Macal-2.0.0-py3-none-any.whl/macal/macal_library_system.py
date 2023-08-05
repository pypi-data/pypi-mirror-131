#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_system.py                                                       #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 System Library                                                                        #
#                                                                                                 #
###################################################################################################

"""System library implementation"""

from .macal_library import PLibrary
from .macal_variable_types import ANY, BOOL, PARAMS, RECORD, STRING
from .macal_expritem import ExpressionItem
from .macal_scope import PScope
from .macal_function import PFunction

class LibrarySystem(PLibrary):
    def __init__(self):
        super().__init__("system")
        self.RegisterFunction("console", [ExpressionItem("arg", PARAMS)], self.Console)
        self.RegisterFunction("record_has_field", [ExpressionItem("rec", RECORD), ExpressionItem("fieldname", STRING)], self.RecordHasField)

    def Console(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func)
        out_str = ""
        # Since the param is type any and we can have any number of them we just iterate over them.
        for param in params:
            out_str = f"{out_str}{param.get_value()}"
        print(out_str)

    def RecordHasField(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of record_has_field function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        result = self.GetParamValue(params, "fieldname") in self.GetParamValue(params, "rec")
        scope.SetReturnValue(result, BOOL)
    