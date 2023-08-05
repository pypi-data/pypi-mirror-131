#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_expritem.py                                                             #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Expression Item Type                                                                  #
#                                                                                                 #
###################################################################################################

"""Expression item class used as value for left and right brances of the expression"""

# mutable variant of ExpressionItem = namedtuple('ExpressionItem', ["value", "item_type"])

class ExpressionItem:
    """Expression item class, used by expressions and interpreter"""
    def __init__(self, value, item_type):
        """Initializes expression item"""
        self.value = value
        self.item_type = item_type
