#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_function.py                                                             #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Function class                                                                        #
#                                                                                                 #
###################################################################################################

"""PFunction class implementation, this class is used by the scope and by the interpreter."""

# Basically mutable version of PFunction = namedtuple("PFunction", ["name", "parameters", "scope", "block"])

class PFunction:
	"""PFunction initialization."""
	def __init__(self, name, parameters, block):
		self.name = name
		self.parameters = parameters
		self.block = block
		self.scope = None
		self.is_extern = False
		self.call_extern = None
