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
from .macal_interpreterconsts import FuncArg
from .macal_scope import PScope
from .macal_function import PFunction

class LibraryCsv(PLibrary):
    def __init__(self):
        super().__init__("CSV")
        self.RegisterFunction("headersToCsv",  [FuncArg("rec", RECORD)], self.HeadersToCsv)
        self.RegisterFunction("valueToCsv",    [FuncArg("rec", RECORD)], self.ValuesToCsv)
        self.RegisterFunction("arrayToCsv",    [FuncArg("arr", ARRAY)],  self.ArrayToCsv)


    def HeadersToCsv(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of HeadersToCsv function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.args)
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
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.args)
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
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func.args)
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
