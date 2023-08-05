#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astifnode.py                                                            #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementation for AST if node used and returned by the parser, separate because it requires importing expr"""

from .macal_parsernodetypes import ELIF, ELSE, IF
from .macal_expr import Expr
from .macal_astnode import AstNode
from .macal_parsernodes import ast_Block

class ast_Elif_branch(AstNode):
    """AST Node: ElIf"""
    def __init__(self, lex_token, condition, block: ast_Block):
        """Initializes ElIf node type"""
        super().__init__(ELIF, lex_token)
        self.condition = condition
        self.block = block
        self.scope = None

    def print(self, indent):
        """Returns string representation of the node"""
        return "ELIF {} {}".format(self.condition.print(self.condition),
                                   self.block.print(indent))

class ast_Else_branch(AstNode):
    """AST Node: Else"""
    def __init__(self, lex_token, block: ast_Block):
        """Initializes else node type"""
        super().__init__(ELSE, lex_token)
        self.block = block
        self.scope = None

    def set_scope(self, scope):
        self.scope = scope

    def print(self, indent):
        """Returns string representation of the node"""
        return "ELSE {}".format(self.block.print(indent))

class ast_If(AstNode):
    """AST Node: If"""
    def __init__(self, lex_token, condition, block: ast_Block):
        """Initializes if node type"""
        super().__init__(IF, lex_token)
        self.condition = condition
        self.block = block
        self.elif_branch = []
        self.else_branch = None
        self.scope = None

    def set_scope(self, scope):
        self.scope = scope

    def add_elif(self, branch: ast_Elif_branch):
        """adds elif branch to the list"""
        self.elif_branch.append(branch)

    def add_else(self, branch: ast_Else_branch):
        """add else branch"""
        self.else_branch = branch

    def has_elif(self):
        """returns true if there are elif nodes."""
        return len(self.elif_branch) > 0

    def has_else(self):
        """returns true if there is an else statement."""
        return self.else_branch is not None

    def print(self, indent):
        """Returns string representation of the node."""
        castr = Expr().print(self.condition)
        tstr = "{}IF {} {}".format(indent, castr, self.block.print(indent))
        if self.has_elif():
            for branch in self.elif_branch:
                tstr = "{} {}".format(tstr, branch.print(indent))
        if self.has_else():
            tstr = "{} {}".format(tstr, self.else_branch.print(indent))
        return tstr
