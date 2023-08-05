#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_time.py                                                         #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Time Library                                                                          #
#                                                                                                 #
###################################################################################################

"""Time library implementation"""
from datetime import datetime
import time

from .macal_library import PLibrary
from .macal_variable_types import ANY, BOOL, INT, STRING
from .macal_parsernodetypes import VARIABLE
from .macal_expritem import ExpressionItem
from .macal_scope import PScope
from .macal_function import PFunction

class LibraryTime(PLibrary):
    def __init__(self):
        super().__init__("time")
        self.RegisterFunction("date_to_unix",   [ExpressionItem("date_str", STRING)], self.DateToUnix)
        self.RegisterFunction("iso_to_unix",    [ExpressionItem("date_str", STRING)], self.IsoToUnix)
        self.RegisterFunction("date_from_unix", [ExpressionItem("seconds", INT)], self.DateFromUnix)
        self.RegisterFunction("iso_from_unix",  [ExpressionItem("seconds", INT)], self.IsoFromUnix)
        self.RegisterFunction("utcnow",         [], self.UtcNow)
        self.RegisterFunction("utcisonow",      [], self.UtcIsoNow)
        self.RegisterFunction("isonow",         [], self.IsoNow)
        self.RegisterFunction("now",            [], self.Now)
        self.NUM_SECONDS_FIVE_MINUTES = 300
        self.NUM_SECONDS_ONE_HOUR = 3600
        self.TIME_FORMAT = '%Y%m%d%H%M%S'
        self.ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        self.ISO_TIME_tzFORMAT = "%Y-%m-%dT%H:%M:%S.0Z"
        self.__stopwatch__ = 0

    def DateToUnix(self, func: PFunction, name: str, params: list, scope: PScope):
        """Convert a date_string of format YYYYMMDDhhmmss to unix time integer.
           Assumes the date string object is UTC time."""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        dt = datetime.strptime(self.GetParamValue(params, "date_str"), self.TIME_FORMAT)
        epoch = datetime(1970, 1, 1)
        result = int((dt - epoch).total_seconds())
        scope.SetReturnValue(result, INT)

    def IsoToUnix(self, func: PFunction, name: str, params: list, scope: PScope):
        """Convert a date_string of format %Y-%m-%dT%H:%M:%S.%f to unix time integer.
           Assumes the date string object is in iso format."""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        dt = datetime.strptime(self.GetParamValue(params, "date_str"), self.ISO_TIME_FORMAT)
        epoch = datetime(1970, 1, 1)
        result = int((dt - epoch).total_seconds())
        scope.SetReturnValue(result, INT)

    def DateFromUnix(self, func: PFunction, name: str, params: list, scope: PScope):
        """Converts time in seconds since UNIX EPOCH to UTC Time format"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        result = time.strftime(self.TIME_FORMAT, time.gmtime(self.GetParamValue(params, "seconds")))
        scope.SetReturnValue(result, STRING)

    def IsoFromUnix(self, func: PFunction, name: str, params: list, scope: PScope):
        """Converts time in seconds since UNIX EPOCH to UTC Time format"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        result = time.strftime(self.ISO_TIME_tzFORMAT, time.gmtime(self.GetParamValue(params, "seconds")))
        scope.SetReturnValue(result, STRING)

    def UtcNow(self, func: PFunction, name: str, params: list, scope: PScope):
        self.ValidateFunction(name, func)
        result = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        scope.SetReturnValue(result, STRING)

    def UtcIsoNow(self, func: PFunction, name: str, params: list, scope: PScope):
        self.ValidateFunction(name, func)
        result = "{}Z".format(datetime.utcnow().isoformat())
        scope.SetReturnValue(result, STRING)

    def IsoNow(self, func: PFunction, name: str, params: list, scope: PScope):
        self.ValidateFunction(name, func)
        result = datetime.now().isoformat()
        scope.SetReturnValue(result, STRING)

    def Now(self, func: PFunction, name: str, params: list, scope: PScope):
        self.ValidateFunction(name, func)
        result = datetime.now().strftime("%Y%m%d%H%M%S")
        scope.SetReturnValue(result, STRING)
