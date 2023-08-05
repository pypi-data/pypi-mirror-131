#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_parsernodes.py                                                          #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementations for AST nodes used and returned by the parser"""

from .macal_lextoken import Token
from .macal_parsernodetypes import (BLOCK, INDEX, VARIABLE, PARAMS, CALL, FUNCTION,
                                  ASSIGN, FOREACH, BREAK, HALT, RETURN)
from .macal_lextokentypes import NEW_ARRAY_INDEX
from .macal_astnode import AstNode

class ast_Block(AstNode):
    """Node for a block of instructions can contain 0 or more instructions."""
    def __init__(self, lex_token):
        """Initializes block node type"""
        super().__init__(BLOCK, lex_token)
        self.closelex_token = None
        self.instruction_list = []

    def close(self, lex_token):
        """closes the node"""
        self.closelex_token = lex_token

    def add_instruction(self, instruction):
        """Adds an instruction to the list of instructions"""
        self.instruction_list.append(instruction)

    def count(self):
        """Returns the number of instructions in the list."""
        return len(self.instruction_list)

    def is_root(self):
        """Returns true if this is the root block, false if it is not."""
        return self.token is None

    def print(self, indent):
        """Returns string representation of the node"""
        old_indent = indent
        if not self.is_root():
            indent = "    {}".format(indent)
        tstr = ""
        for instr in self.instruction_list:
            tstr = "{}{}\n".format(tstr, instr.print(indent))
        if not self.is_root():
            tstr = "{{\n{}{}}}".format(tstr, old_indent)
        return tstr

class ast_list_Index(AstNode):
    """AST Node: Index"""
    def __init__(self, lex_token, expression, closelex_token):
        """Initializes index node type"""
        super().__init__(INDEX, lex_token)
        self.expr = expression
        self.closelex_token = closelex_token

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{} [".format(indent)
        if self.expr is not None:
            tstr = "{} {}".format(tstr, self.expr.print(self.expr))
        return "{} ]".format(tstr)

class ast_Variable(AstNode):
    """AST Node: Variable"""
    def __init__(self, lex_token):
        """Initializes variable node type"""
        super().__init__(VARIABLE, lex_token)
        self.index       = []
        self.value       = None
        self.initialized = False

    def set_value(self, value):
        """sets the value, and also sets the initialized flag"""
        self.initialized = True
        self.value = value

    def add_index(self, index: ast_list_Index):
        """add an index to the list of indexies"""
        self.index.append(index)

    def has_index(self):
        """Returns true if indexes exist on the list"""
        return len(self.index) > 0

    def is_initialized(self):
        """Returns true if this variable was initialized"""
        return self.initialized

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{}VARIABLE: {}".format(indent, self.name())
        if self.has_index():
            for i in self.index:
                tstr = "{} {}".format(tstr, i.print(""))
        if self.value is not None:
            tstr = "{} {}".format(tstr, self.value.print(self.value))
        return tstr

class ast_function_Param_list(AstNode):
    """AST Node: Parameter list"""
    def __init__(self, lex_token):
        """Initializes parameter list node type"""
        super().__init__(PARAMS, lex_token)
        self.closelex_token = None
        self.params = []

    def close(self, lex_token):
        """closes the node"""
        self.closelex_token = lex_token

    def add_parameter(self, expression):
        """adds a parameter to the list"""
        self.params.append(expression)
        
    def count(self):
        """returns the number of parameters on the list"""
        return len(self.params)

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{}(".format(indent)
        cnt = len(self.params)
        i = 0
        for expr in self.params:
            tstr = "{}{}".format(tstr, self._print_expr(expr))
            if i < cnt-1:
                tstr = "{}, ".format(tstr)
            i += 1
        tstr = "{})".format(tstr)
        return tstr
    
class ast_Call_function(AstNode):
    """AST Node: Call"""
    def __init__(self, tid: ast_Variable, params: ast_function_Param_list):
        """Initializes function call node type"""
        super().__init__(CALL, tid.token)
        self.ident = tid
        self.params = params

    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()

    def print(self, indent):
        """Returns string representation of the node"""
        name = self.name()
        params = self.params.print("")
        return "{}CALL {} {}".format(indent, name, params)

class ast_Function_definition(AstNode):
    """AST Node: Function"""
    def __init__(self, tid: ast_Variable, opLex: Token, params: ast_function_Param_list,
                 block: ast_Block):
        """Initializes function definition node type"""
        super().__init__(FUNCTION, tid.token)
        self.operand = opLex
        self.ident = tid
        self.params = params
        self.block = block
        self.isextern = False
        self.extern_call = None

    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()

    def print(self, indent):
        """Returns string representation of the node"""
        myname = self.name()
        myparams = self.params.print("")
        myblock = self.block.print(indent)
        return "{}FUNCTION {} {} {}".format(indent, myname, myparams, myblock)

class ast_Assign(AstNode):
    """AST Node: Assign"""
    def __init__(self, operand, tid: ast_Variable, expression):
        """Initializes assign node type"""
        super().__init__(ASSIGN, tid.token)
        self.operand = operand
        self.ident = tid
        self.expr = expression
        self.ref = False
        self.ref_token = None

    def print(self, indent):
        """Returns string representation of the node"""
        name = self.ident.name()
        if self.ref:
            name = "REF: {}".format(name)
        if self.ident.has_index():
            for idx in self.ident.index:
                left = idx.expr.left.value
                if left == NEW_ARRAY_INDEX:
                    name = "{}[]".format(name)
                else:
                    name = "{}[{}]".format(name, left)
        operand = self.operand[1]
        expr = self._print_expr(self.expr)
        return "{}ASSIGN {} {} {}".format(indent, name, operand, expr)

class ast_Foreach(AstNode):
    """AST Node: ForEach"""
    def __init__(self, lex_token, expression, block: ast_Block):
        """Initializes foreach node type"""
        super().__init__(FOREACH, lex_token)
        self.expr = expression
        self.block = block
        self.iterator_var = None

    def print(self, indent):
        """Returns string representation of the node"""
        return "{}FOREACH {} {}".format(indent, self._print_expr(self.expr),
                                        self.block.print(indent))

class ast_Break(AstNode):
    """AST Node: Break"""
    def __init__(self, lex_token):
        """Initializes break node type"""
        super().__init__(BREAK, lex_token)
    
    def print(self, indent):
        """Returns string representation of the node"""
        return "{}{}".format(indent, self.node_type)

class ast_Halt(AstNode):
    """AST Node: Halt"""
    def __init__(self, lex_token, expression):
        """Initializes halt node type"""
        super().__init__(HALT, lex_token)
        self.expr = expression

    def print(self, indent):
        """Returns string representation of the node"""
        return "{}HALT {}".format(indent, self._print_expr(self.expr))

class ast_Return(AstNode):
    """AST Node: Return"""
    def __init__(self, lex_token, expression):
        """Initializes return node type"""
        super().__init__(RETURN, lex_token)
        self.expr = expression

    def print(self, indent):
        """Returns string representation of the node"""
        return "{}RETURN {}".format(indent, self._print_expr(self.expr))

