#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_lextoken.py                                                             #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Named tuples used for return values by lexer and parser                               #
#                                                                                                 #
###################################################################################################

""""Named tuples used for function return values"""

from collections import namedtuple

# Location tuple used to keep track of the location of a token, and/or the current position in the
# source code.
Location = namedtuple('Location', ["pos", "line", "offset"])

# Actual lexer token consists of a type, value and location where location is of type Location to
# indicate where in the source code the token is.
Token = namedtuple('Token', ["type", "value", "location"])

SingleToken = namedtuple("SingleToken", ["value", "type"])

# Used by the parser to split each parameter in the select statement by it's token, astoken and
# asvalue. token being having the name of a field as value or * for any.
# Astoken being the "as" keyword, asvalue being the token that has the destination name of the
# field.
SelectParam = namedtuple('SelectParam', ['token', 'astoken', 'asvalue'])

Some = namedtuple('Some', ['value', 'location'])
