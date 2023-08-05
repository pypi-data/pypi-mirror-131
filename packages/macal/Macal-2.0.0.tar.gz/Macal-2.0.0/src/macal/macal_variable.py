#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_variable.py                                                             #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Variable class                                                                        #
#                                                                                                 #
###################################################################################################

"""PVariable class implementation, this class is used by the scope and by the interpreter."""

class PVariable:
	"""PVariable has to be a class because a named tuple is not mutable after it was set."""
	def __init__(self, name):
		self.name  = name
		self.x_value = None
		self.x_var_type = None
		self.initialized = False

	def get_value(self):
		return self.x_value

	def set_value(self, value):
		self.x_value = value
		self.initialized = True

	def get_type(self):
		return self.x_var_type

	def set_type(self, var_type):
		self.x_var_type = var_type
