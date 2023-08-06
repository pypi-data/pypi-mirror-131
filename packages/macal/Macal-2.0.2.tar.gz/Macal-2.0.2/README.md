# Macal Package

This is the installation package for Macal, a Python script Language by Marco Caspers.

Macal was developed for a limited and specific use.

Creating a human and machine readable configuration file that loads data, transforms the data and emits the data.
Loading happens by calling functions from libraries specific to a particular (Rest/XML) API.

Emitting data is currently limited to the console and SysLog.

In the tests folder find the test.py utility that contains several tests.

13-12-2021:
Please note that this package was previously called pyql, however there already existed a pyql project so i renamed it.

Whats new in 2.0:

- Fully revised lexer, parser and interpreter.
- Script language now support defining functions.
- The interface for libraries was changed to make it much easier to write libraries.
- Published on github in a private repository.
- Extension for examples changed from .pyql into .mcl
- Examples in example subfolder
- Removed http library, may be re-added later
- Removed external dependancies due to removal of http library
- Changed interface of syslog commands

Version 2.0.1:
- Minor bugfix, validatefunction throws an exception which needed scope to be passed, but the function didn't have that arg.
- Function Parameters/Arguments for library RegisterFunction now created by FuncArg() instead of ExpressionItem() to 
  make the name more obvious and easier to read.