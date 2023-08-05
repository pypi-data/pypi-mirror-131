#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_io.py                                                           #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 IO Library                                                                            #
#                                                                                                 #
###################################################################################################

"""IO library implementation"""

import os
from .macal_library import PLibrary
from .macal_variable_types import BOOL, STRING
from .macal_expritem import ExpressionItem
from .macal_scope import PScope
from .macal_function import PFunction

class LibraryIO(PLibrary):
    def __init__(self):
        super().__init__("io")
        self.RegisterFunction("load",         [ExpressionItem("filename", STRING)], self.Load)
        self.RegisterFunction("exists",       [ExpressionItem("filename", STRING)], self.Exists)
        self.RegisterFunction("save",         [ExpressionItem("content", STRING), ExpressionItem("filename", STRING)], self.Save)
        self.RegisterFunction("get_last_run", [ExpressionItem("org_name", STRING), ExpressionItem("iso_now", STRING)], self.GetLastRun)
        self.RegisterFunction("set_last_run", [ExpressionItem("org_name", STRING), ExpressionItem("iso_now", STRING)], self.SetLastRun)

    def Load(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of Load function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        filename = self.GetParamValue(params, "filename")
        with open (filename, "r") as tf:
            content=tf.read()
        scope.SetReturnValue(content, STRING)

    def Exists(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of Exists function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        filename = self.GetParamValue(params, "filename")
        result = os.path.exists(filename)
        scope.SetReturnValue(result, BOOL)

    def Save(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of Save function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        content  = self.GetParamValue(params, "content")
        filename = self.GetParamValue(params, "filename")
        with open(filename, "w") as tf:
            tf.write(content)	

    def GetLastRun(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of GetLastRun function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        org_name = self.GetParamValue(params, "org_name")
        iso_now  = self.GetParamValue(params, "iso_now")

        fileName = "/tmp/last_run_{}.ctl".format(org_name);
        if os.name == "nt":
            fileName = "c:/temp/last_run_{}.ctl".format(org_name);
        if os.path.exists(fileName):
            with open (fileName, "r") as tf:
                result=tf.read()
            if result is None or result == '':
                result = iso_now
        else:
            result = iso_now
        scope.SetReturnValue(result, STRING)

    def SetLastRun(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of SetLastRun function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        org_name = self.GetParamValue(params, "org_name")
        iso_now  = self.GetParamValue(params, "iso_now")
        fileName = "/tmp/last_run_{}.ctl".format(org_name);
        if os.name == "nt":
            fileName = "c:/temp/last_run_{}.ctl".format(org_name);
        with open(fileName, "w") as tf:
            tf.write(iso_now)
