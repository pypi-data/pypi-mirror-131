#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_astselectnode.py                                                        #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 AST Node classes instantiated by the parser                                           #
#                                                                                                 #
###################################################################################################

"""Implementation for AST node select used and returned by the parser, it is separate because it requires importing expr"""

from .macal_parsernodetypes import SELECT
from .macal_expr import Expr
from .macal_astnode import AstNode

class ast_Select(AstNode):
    """AST Node: Select"""
    def __init__(self, lex_token, params: list, pfrom: Expr, into: Expr):
        """Initializes select node type"""
        super().__init__(SELECT, lex_token)
        self.distinct = False
        self.params = params
        #self.from_token = None
        self.sfrom = pfrom
        self.where_token = None
        self.where = None
        self.merge = None
        #self.into_token = None
        self.into = into

    def set_distinct(self, distinct: bool):
        """sets optional distinct flag"""
        self.distinct = distinct

    def set_where(self, where_token, where_value):
        """Sets optional where statement"""
        self.where_token = where_token
        self.where = where_value

    def set_merge(self, merge):
        """sets optional merge statement"""
        self.merge = merge

    def _print_params(self):
        """Returns string representation of the parameters"""
        tstr = ""
        if self.distinct:
            tstr = "DISTINCT "
        count = len(self.params)
        idx = 0
        for param in self.params:
            tstr = "{}{}".format(tstr, param.token.value)
            if param.asvalue is not None:
                tstr = "{} AS {}".format(tstr, param.asvalue.value)
            if idx < count-1:
                tstr = "{}, ".format(tstr)
        return tstr

    def _print_where(self):
        """Returns string representation of the where instruction if it exists"""
        if self.where is None:
            return ""
        return "WHERE {}".format(self._print_expr(self.where))

    def print(self, indent):
        """Returns string representation of the node"""
        tstr = "{}SELECT {} FROM {} {}".format(indent, self._print_params(),
                                               self._print_expr(self.sfrom), self._print_where())
        if self.merge:
            tstr = "{} MERGE".format(tstr)
        tstr = "{} INTO {}".format(tstr, self._print_expr(self.into))
        return tstr
