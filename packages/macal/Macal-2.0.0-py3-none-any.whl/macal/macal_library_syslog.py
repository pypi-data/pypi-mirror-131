#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_library_syslog.py                                                       #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Syslog Library                                                                        #
#                                                                                                 #
###################################################################################################

"""Syslog library implementation"""

from .macal_library import PLibrary
from .macal_variable_types import STRING, BOOL, INT
from .macal_expritem import ExpressionItem
from .macal_scope import PScope
from .macal_function import PFunction
from .macal_SysLog_class import SysLog

class LibrarySyslog(PLibrary):
    def __init__(self):
        super().__init__("syslog")
        self.RegisterFunction("syslog",             [ExpressionItem("level", STRING), ExpressionItem("message", STRING)], self.Syslog)
        self.RegisterFunction("syslog_init",        [ExpressionItem("remote", BOOL)], self.SyslogInit)
        self.RegisterFunction("syslog_set_address", [ExpressionItem("address", STRING), ExpressionItem("port", INT)], self.SyslogSetAddress)
        self.SysLog = SysLog()
        
    def Syslog(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of Syslog function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        level = self.GetParamValue(params, "level")
        message = self.GetParamValue(params, "message")
        if level == "debug":
            self.SysLog.debug(message)
        elif level == "info" or level == "information":
            self.SysLog.info(message)
        elif level == "warn" or level == "warning":
            self.SysLog.warn(message)
        elif level == "error":
            self.SysLog.error(message)
        elif level == "critical":
            self.SysLog.critical(message)
        else:
            raise Exception(f"Invalid syslog level given: {level}")

    def SyslogInit(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of SysLog init function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        remote = self.GetParamValue(params, "remote")
        self.SysLog.SysLogInit(remote)

    def SyslogSetAddress(self, func: PFunction, name: str, params: list, scope: PScope):
        """Implementation of SysLog SetAddress function"""
        self.ValidateFunction(name, func)
        self.ValidateParams(name, params, scope, func.parameters)
        address = self.GetParamValue(params, "address")
        port = self.GetParamValue(params, "port")
        self.SysLog.SysLogSetAddress(address, port)