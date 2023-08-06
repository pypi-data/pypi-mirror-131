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

class PFunction:
	"""PFunction initialization."""
	def __init__(self, name: str, args: list, block):
		self.name = name
		self.args = args
		self.block = block
		self.scope = None
		self.is_extern = False
		self.call_extern = None
