#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_csv.py                                                          #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 CSV Library                                                                           #
#                                                                                                 #
###################################################################################################

"""CSV library implementation"""

from .macal_library import PLibrary
from .macal_variable_types import ARRAY, RECORD, STRING
from .macal_expritem import ExpressionItem
from .macal_scope import PScope
from .macal_function import PFunction
from .macal_SysLog_class import SysLog

class LibraryCsv(PLibrary):
    def __init__(self):
        super().__init__("CSV")
        self.RegisterFunction("headersToCsv",             [ExpressionItem("rec", RECORD)], self.HeadersToCsv)
        self.RegisterFunction("valueToCsv",        [ExpressionItem("rec", RECORD)], self.ValuesToCsv)
        self.RegisterFunction("arrayToCsv", [ExpressionItem("arr", ARRAY)], self.ArrayToCsv)


    def HeadersToCsv(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of HeadersToCsv function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        rec = self.GetParamValue(params, "rec")
        result = None
        try:
            separator = '","'
            result = f'"{separator.join(rec)}"'
        except Exception as e:
            raise RuntimeError(e)
        scope.SetReturnValue(result, STRING)

    def ValuesToCsv(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of ValuesToCsv function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        rec = self.GetParamValue(params, "rec")
        result = None
        try:
            temp = []
            for fld in rec:
                temp.append('"{}"'.format(rec[fld]))
            separator = ','
            result = separator.join(temp)
        except Exception as e:
            raise RuntimeError(e)
        scope.SetReturnValue(result, STRING)

    def ArrayToCsv(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of ArrayToCsv function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        arr = self.GetParamValue(params, "arr")
        try:
            temp = []
            for fld in arr:
                temp.append('"{}"'.format(fld))
            separator = ','
            result = separator.join(temp)
        except Exception as e:
            raise RuntimeError(e)
        scope.SetReturnValue(result, STRING)
