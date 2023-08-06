#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astnode.py                                                              #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AstNode base class                                                                    #
#                                                                                                 #
###################################################################################################

"""Abstract base class AstNode used as a base for various ast node types."""

from abc import ABC, abstractmethod

class AstNode(ABC):
    """node ancestor for all other node types"""
    def __init__(self, node_type, lex_token):
        """Base AST node, all other node types inherit this one."""
        self.type = node_type
        self.token = lex_token

    def name(self):
        """returns token name"""
        return self.token.value

    def node_type(self):
        """returns node type"""
        return self.type
    
    @staticmethod
    def _print_expr(expr):
        """Determines if the passed expression is of actual expression type or a node type and
        calls/returns the apropriate print instruction for that type."""
        if expr is not None:
            if issubclass(type(expr), AstNode):
                return expr.print("")
            return expr.print(expr)
        return ""

    @abstractmethod
    def print(self, indent):
        pass
