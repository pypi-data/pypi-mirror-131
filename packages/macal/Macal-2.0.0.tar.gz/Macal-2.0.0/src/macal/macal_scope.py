#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_scope.py                                                                #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Expression node class                                                                 #
#                                                                                                 #
###################################################################################################

"""Scope class implementation, this class is used by the interpreter."""

from .macal_variable_types import ANY, ARRAY, BOOL, FLOAT, INT, STRING, RECORD
from .macal_keywords import NIL
from .macal_variable import PVariable
from .macal_function import PFunction

VARIABLE_COLUMN_WIDTH = 40
TYPE_COLUMN_WIDTH     = 12
VALUE_COLUMN_WIDTH    = 36

class PScope:
    """Scope class implements execution branch scope"""
    def __init__(self, name: str, parent):
        self.name = name
        self.variables:   list[PVariable] = []
        self.functions:   list[PFunction] = []
        self.children:    list[PScope]    = []
        self.break_flag:  bool            = False
        self.x_halt_flag: bool            = False
        self.is_loop:     bool            = False
        self.parent:      PScope          = parent
        self.Libraries:   list            = []

    def create_child(self, name: str):
        child = PScope("{}->{}".format(self.name, name), self)
        self.children.append(child)
        return child

    def remove_child(self, child):
        self.children.remove(child)
    
    def set_halt(self):
        self.x_halt_flag = True

    def get_halt(self):
        return self.x_halt_flag

    def add_new_variable(self, name: str):
        """Adds a new PVariable to the scope and returns it."""
        variable = PVariable(name)
        self.variables.append(variable)
        return variable

    def add_new_function(self, name: str, parameters, block):
        """Adds a new PFunction to the scope and returns it."""
        func = PFunction(name, parameters, block)
        self.functions.append(func)
        return func
    
    @staticmethod
    def _obj_first_or_default(lst: list, name: str):
        """Returns the first object in the list that has name, or None if not found."""
        return next((x for x in lst if x.name == name), None)
    
    def _get_variable(self, name: str):
        """Find variable by name in the current scope"""
        return next((x for x in self.variables if x.name == name), None)

    def _get_function(self, name: str):
        """Find function by name in the current scope"""
        return next((x for x in self.functions if x.name == name), None)

    def _get_scope_exitvar(self):
        for var in self.variables:
            if var.name[:8] == "?return_":
                return var
        return None

    def SetReturnValue(self, value, valuetype):
        var = self._get_scope_exitvar()
        if var is None:
            raise Exception(f"This scope has no exitvar! {self}")
        var.set_value(value)
        var.set_type(valuetype)

    def _find_variable(self, name: str, scope):
        """Find variable by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        var = scope._get_variable(name)
        if var is not None:
            return var
        if scope.parent is not None and scope.parent.has_variables():
            return self._find_variable(name, scope.parent)
        return None

    def _find_function(self, name: str, scope):
        """Find function by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        func = scope._get_function(name)
        if func is not None:
            return func

        if len(self.Libraries) > 0:
            for lib in self.Libraries:
                func = lib.GetFunction(name)
                if func is not None:
                    return func

        if scope.parent is not None and scope.parent.has_functions():
            return self._find_function(name, scope.parent)
        return None

    def find_variable(self, name: str):
        return self._find_variable(name, self)
    
    def find_function(self, name: str):
        return self._find_function(name, self)
    
    def has_children(self):
        return len(self.children) > 0

    def has_variables(self):
        return len(self.variables) > 0

    def has_functions(self):
        return len(self.functions) > 0

    def print_variables(self):
        """Displays a table showing all variables in this scope."""
        # define the column width
        variable_size = VARIABLE_COLUMN_WIDTH
        type_size     = TYPE_COLUMN_WIDTH
        value_size    = VALUE_COLUMN_WIDTH
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        print("|{}|{}|{}|".format(
            "Variable".ljust(variable_size),
            "Type".ljust(type_size),
            "Value".ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        for var in self.variables:
            vt = var.get_type()
            vts = '{}'.format(vt)
            vv = repr(var.get_value())
            if isinstance(vv, PFunction):
                vv = vv.name
            print("|{}|{}|{}|".format(var.name.ljust(variable_size), vts.ljust(type_size), '{}'.format(vv).ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))

    @staticmethod
    def get_value_type(obj):
        """returns a string representing the given object type"""
        result = "unknown"
        if obj is None:
            result = NIL
        elif isinstance(obj, bool):
            result = BOOL
        elif isinstance(obj, int):
            result = INT
        elif isinstance(obj, float):
            result = FLOAT
        elif isinstance(obj, str):
            result = STRING
        elif isinstance(obj, list):
            result = ARRAY
        # ToDo: Add dictionaries to the language.
        elif isinstance(obj, dict):
            result = "RECORD"
        # the following types should never happen, but i added them in to be complete.
        elif isinstance(obj, complex):
            result = "complex"
        elif isinstance(obj, tuple):
            result = "tuple"
        elif isinstance(obj, bytes):
            result = "bytes"
        elif isinstance(obj, bytearray):
            result = "bytearray"
        elif isinstance(obj, set):
            result = "set"
        elif isinstance(obj, frozenset):
            result = "frozenset"
        else:
            raise Exception("Unknown type: {}".format(type(obj)))
        return result
    
    def print(self, scope):
        print("\nScope: ", scope.name)
        if scope.has_variables():
            scope.print_variables()
        if scope.has_children():
            for child in scope.children:
                self.print(child)
