#!/usr/bin/python3
#-------------------------------------------------------------------------------------------------#
# Filename:       | __init__.py                                                                   #
# Author:         | Marco Caspers                                                                 #
# Date:           | 13-12-2021                                                                    #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 language Initialization                                                               #
#                                                                                                 #
###################################################################################################

"""macal Main class implementation"""

from .macal_lexer import PLexer
from .macal_parser import PParser
from .macal_interpreter import PInterpreter
from .macal_library import PLibrary

__version__ = "2.0"
__author__ = "Marco Caspers"
__credits__ = "Copyright (c) 2021 Westcon Security Netherlands"

class macal:
    """macal Language"""
    def __init__(self):
        """Initializes macal Language class"""
        self.lexer       = PLexer(None)
        self.parser      = PParser()
        self.interpreter = PInterpreter()
        self.source      = None
        self.tokens      = None
        self.ast_tree    = None
        self.debug       = False
        self.print_tree  = False
        self.print_scope = False
        self.scope       = self.interpreter.scope
        self.Libraries:  list[PLibrary] = []
        self.scope.Libraries = self.Libraries

    def run_from_file(self, filename, **kwargs):
        """Runs the language using a file as input"""
        try:
            with open (filename, mode = 'r', encoding = 'utf-8') as text_file:
                source = text_file.read()
            return self.run_from_string(source, **kwargs)
        except FileNotFoundError:
            raise Exception("@Runtime error: File not found: {}".format(filename))

    def register_library(self, lib: PLibrary):
        self.Libraries.append(lib)

    def register_variable(self, name: str, value, vartype):
        var = self.interpreter.scope.add_new_variable(name)
        var.set_value(value)
        var.set_type(vartype)
        return var

    def run_from_string(self, source): #, **kwargs):
        """Runs the language using a string as input"""
        #for name, value in kwargs.items():
        #	self.Scope.SetVarValue(name, value, None)
        self.source = source
        self.tokens   = self.lexer.lex(self.source)
        self.ast_tree = self.parser.parse(self.tokens)
        if self.debug and self.print_tree:
            print(self.ast_tree.print(""))
        #run interpreter
        result = self.interpreter.interpret(self.ast_tree)

        if self.debug and self.print_scope:
            self.interpreter.scope.print(self.interpreter.scope)

        return result

    def versions(self):
        """Returns the versions of all individual modules that make up the language."""
        vstr = "Macal version:       {}\r\n".format(__version__)
        vstr = "{}Tokenizer version:   {}\r\n".format(vstr, self.lexer.version)
        vstr = "{}Parser version:      {}\r\n".format(vstr, self.parser.version)
        vstr = "{}interpreter version: {}\r\n\r\n".format(vstr, self.interpreter.version)
        vstr = "{}libraries:\n".format(vstr)
        for lib in self.Libraries:
        	vstr = "{}{:<10}           {}\r\n".format(vstr, lib.name, lib.version)
        return vstr
