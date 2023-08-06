#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_expr.py                                                                 #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Expression node class                                                                 #
#                                                                                                 #
###################################################################################################

"""Expression class implementation, this class is used by the parser."""

from .macal_lextokentypes import IDENTIFIER
from .macal_exprtypes import BINARY, UNARY, LITERAL, GROUPING, VARIABLE, INDEX, FUNCTION, PARAMS
from .macal_parsernodetypes import CALL
from .macal_keywords import NIL
from .macal_expritem import ExpressionItem

class Expr:
    """Expression class with static methods to instantiate specific expr node types."""
    def __init__(self):
        """Base initializer for Expr class"""
        self.expr_type  = None
        self.left       = ExpressionItem(None, NIL)
        self.operator   = None
        self.right      = ExpressionItem(None, NIL)

    def set_right(self, value):
        """set right parameter"""
        self.right = value

    @staticmethod
    def binary(left, operator, right):
        """Instantiates Expr node of type binary"""
        instance = Expr()
        instance.expr_type = BINARY
        instance.left = ExpressionItem(left, Expr)
        instance.operator = operator
        instance.right = ExpressionItem(right, Expr)
        return instance

    @staticmethod
    def unary(operator, right):
        """Instantiates Expr node of type unary"""
        instance = Expr()
        instance.expr_type = UNARY
        instance.operator = operator
        instance.right = ExpressionItem(right, Expr)
        return instance

    @staticmethod
    def literal(left):
        """Instantiates Expr node of type literal"""
        instance = Expr()
        instance.expr_type = LITERAL
        instance.left = left
        return instance

    @staticmethod
    def grouping(grouping):
        """Instantiates Expr node of type grouping"""
        instance = Expr()
        instance.expr_type = GROUPING
        instance.left = ExpressionItem(grouping, GROUPING)
        return instance

    @staticmethod
    def variable(var):
        """Instantiates Expr node of type variable"""
        instance = Expr()
        instance.expr_type = VARIABLE
        instance.left = ExpressionItem(var, VARIABLE)
        return instance

    @staticmethod
    def index(index):
        """Instantiates Expr node of type variableindex"""
        instance = Expr()
        instance.expr_type = INDEX
        instance.left = ExpressionItem(index, INDEX)
        return instance

    @staticmethod
    def function(fun):
        """Instantiates Expr node of type function call"""
        instance = Expr()
        instance.expr_type = FUNCTION
        instance.left = ExpressionItem(fun, CALL)
        instance.operator = CALL
        return instance

    @staticmethod
    def param_list():
        """Instantiates Expr node of type parameter list."""
        instance = Expr()
        instance.expr_type = PARAMS
        instance.left = ExpressionItem([], PARAMS)
        return instance
    
    def print(self, expr):
        """Recursive printing function to display the entire expression"""
        if expr is None:
            return ""
        result = ""
        if isinstance(expr, tuple):
            if expr[0] == IDENTIFIER:
                result = expr[1]
            else:
                result = "Unknown {}".format(expr[0])
        elif not isinstance(expr, Expr) and expr is not None:
            result = expr.print("")
        elif expr.expr_type == BINARY:
            result = "( {} op: {} {})".format(self.print(expr.left.value),
                                              expr.operator, self.print(expr.right.value))
        elif expr.expr_type == UNARY:
            uop = expr.operator
            uright = expr.right.value
            result = "(unop: {} {})".format(uop, self.print(uright))
        elif expr.expr_type == LITERAL:
            result = repr("{}: {}".format(expr.left.item_type, expr.left.value))
        elif expr.expr_type == GROUPING:
            result = "( {} )".format(self.print(expr.left.value))
        elif expr.expr_type == INDEX:
            result = "Index [ {} ]".format(expr.left.value)
        elif expr.expr_type == FUNCTION:
            result =self.print(expr.left.value)
        #elif (expr.expr_type == VARIABLE):
        #    result = expr.print()
        #elif (expr.expr_type == PARAMS):
        #    result = expr.print()
        else:
            result = "Unknown {}".format(expr.expr_type)
        return result
