#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_lexer.py                                                                #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Language Lexer                                                                        #
#                                                                                                 #
###################################################################################################

"""Lexer implementation"""

from string import whitespace

from .macal_lextoken import Token, Location, Some
from .macal_lextokentypes import (SINGLETOKENS, OP_DIV, OP_EQUAL, OP_ASSIGN, OP_LT, OP_LTEQUAL,
                               OP_GT, OP_NOT, OP_GTEQUAL, OP_NOTEQUAL, OP_DEFINE, IDENTIFIER, KEYWORD, 
                               COMMENT, ERROR, COLON)
from .macal_variable_types import ANY, ARRAY, BOOL, FLOAT, INT, STRING, RECORD
from .macal_keywords import Keywords, TRUE, FALSE, NIL

class PLexer:
    """macal Language Lexer class"""
    def __init__(self, source):
        """Initializers lexer with source code"""
        self.source  = source
        self.version = "2.0"
        self.line_end = '\n'
        self.length = 0
        if source is not None:
            self.length  = len(source)

    def _get_current_char(self, location: Location):
        """Returns the current character, advances the position to the next character if possible,
        also updates line and offset. Returns None if position is equal or greater than the length
        of the source."""
        if location.pos < self.length:
            if self.source[location.pos] == self.line_end:
                return Some(self.source[location.pos],
                            Location(location.pos+1, location.line+1, 0))
            return Some(self.source[location.pos],
                Location(location.pos+1, location.line, location.offset+1))
        return None

    def _skip_char(self, char, location: Location):
        """Skips the current character if it is the given character. Returns None if end of
        source or the character doesn't match."""
        current = self._get_current_char(location)
        if isinstance(current, Some) and current.value == char:
            return current
        return None

    def _get_letter(self, location: Location):
        """validate if the current character is a letter (a-zA-Z) and returns it, or returns
        None if end of source or if it's not a letter."""
        current = self._get_current_char(location)
        if isinstance(current, Some) and current.value.isalpha():
            return current
        return None

    def _get_digit(self, location: Location):
        """validate if the current character is a digit (0-9) and returns it, or returns None if
        end of source or if it's not a digit."""
        current = self._get_current_char(location)
        if isinstance(current, Some) and current.value.isdigit():
            return current
        return None

    def _get_letter_or_digit(self, location: Location):
        current = self._get_current_char(location)
        if isinstance(current, Some) and (current.value.isalpha() or current.value.isdigit()):
            return current
        return None
    
    def _get_in_list(self, lst: list, location: Location):
        """Checks if the current character is in the allowed list and returns it if it is so,
        returns none if not matched or end of source was reached."""
        current = self._get_current_char(location)
        if isinstance(current, Some) and current.value in lst:
            return current
        return None

    @staticmethod
    def _or_else(func, sfunc, location: Location):
        """Runs first given function with pos, line and offset parameters. If that function
        returned a value, that value is returned. If the first function returned None, the
        second function is ran with the same parameters and its return value is returned.
        Please note that this may still return for None to be returned."""
        result = func(location)
        if isinstance(result, Some):
            return result
        return sfunc(location)

    def _or_else_in_list(self, func, sfunc, lst, location: Location):
        func_result = self._or_else(func, sfunc, location)
        if func_result is None:
            func_result = self._get_in_list(lst, location)
        return func_result

    @staticmethod
    def _many(func, location: Location):
        """scans the source with function, if the function returns None the scanning is
        stopped. Adds the result of the function to a list which is returned when the function
        returned None. This may result in an empty list being returned."""
        func_result = func(location)
        current_loc = location
        aggr = []
        while func_result is not None:
            aggr.append(func_result.value)
            current_loc = func_result.location
            func_result = func(current_loc)
        return Some(aggr, current_loc)
    
    def _many_or_in_list(self, func, sfunc, lst: list, location: Location):
        """The same as if running _many with _or_else_in_list"""
        func_result = self._or_else_in_list(func, sfunc, lst, location)
        current_loc = location
        aggr = []
        while func_result is not None:
            aggr.append(func_result.value)
            current_loc = func_result.location
            func_result = self._or_else_in_list(func, sfunc, lst, current_loc)
        return Some(aggr, current_loc)

    def _any_until(self, lst: list, location: Location):
        """Scans source and returns any found character in a list up until the passed
        character (no) is found."""
        aggr = []
        current_loc = location
        current = self._get_current_char(current_loc)
        while current is not None:
            if isinstance(current, Some) and current.value not in lst:
                aggr.append(current.value)
                current_loc = current.location
            else:
                break
            current = self._get_current_char(current_loc)
        return Some(aggr, current_loc)

    def _skip_whitespace(self, location: Location):
        """scans the source for whitespaces from current position and skips them if found,
        otherwise returns the first position past the whitespace"""
        current_loc = location
        current = self._get_current_char(current_loc)
        while isinstance(current, Some) and current.value in whitespace:
            current_loc = current.location
            current = self._get_current_char(current_loc)
        return current_loc

    @staticmethod
    def _convert_to_string(lst):
        """converts a list of characters into a string while honoring escape sequences!, 
           a simple join will destroy escape sequecnes and it's impossible to fix afterwards."""
        if isinstance(lst, list):
            ctstr = ""
            index = 0
            length = len(lst)
            while index < length:
                if lst[index] == '\\' and index < length-1 and lst[index+1] in ['a','b','n','r','t','0']:
                    if lst[index+1] == 'a':
                        ctstr += '\a'
                    elif lst[index+1] == 'b':
                        ctstr += '\b'
                    elif lst[index+1] == 'n':
                        ctstr += '\n'
                    elif lst[index+1] == 'r':
                        ctstr += '\r'
                    elif lst[index+1] == 't':
                        ctstr += '\t'
                    elif lst[index+1] == '0':
                        ctstr += '\0'
                    index+=1
                else:
                    ctstr += lst[index]
                index += 1
            return ctstr
        return None

    @staticmethod
    def _convert_to_int(lst):
        """Converts a list of digits into an 'integer'"""
        value = 0
        for char in lst:
            value = value * 10 + ord(char) - ord('0')
        return value

    @staticmethod
    def _is_keyword(kwd):
        """Returns only true if the given kwd is in the list of keywords"""
        if kwd in Keywords:
            return True
        return False

    def _get_identifier(self, location: Location, first: Some):
        """getIdentifier scans the input source for a valid identifier.
           The scanned identifier is checked to be a boolean value, nil, or a keyword and
           returns the apropriate type of token if matched, or simply token of type identifier
           if none of those other three types are found."""
        aggr = []
        aggr.append(first.value)
        current_loc = first.location
        current = self._many_or_in_list(self._get_letter, self._get_digit, ['_'], current_loc)
        if isinstance(current, Some):
            aggr.extend(current.value)
            current_loc = current.location
        ident = self._convert_to_string(aggr)
        if ident in (TRUE, FALSE):
            result = Some(Token(BOOL, ident, location), current_loc)
        elif ident == NIL:
            result = Some(Token(NIL, ident, location), current_loc)
        elif self._is_keyword(ident):
            result = Some(Token(KEYWORD, ident, location), current_loc)
        else:
            result = Some(Token(IDENTIFIER, ident, location), current_loc)
        return result

    def _get_literal_number_token(self, location: Location):
        number = self._many(self._get_digit, location)
        if not isinstance(number, Some):
            return None
        value = self._convert_to_int(number.value)
        current_loc = number.location
        peek = self._get_current_char(current_loc)
        if not isinstance(peek, Some) or peek.value != '.':
            return Some(Token(INT, value, location), current_loc)
        
        result = self._many(self._get_digit, peek.location)
        if not isinstance(result, Some):
            return Some(Token(ERROR, "Unexpected character in float", current_loc), peek.location)
        factor = 0.1
        for digit in result.value:
            value = value + (factor * (ord(digit)-ord('0')))
            factor = factor / 10
        return Some(Token(FLOAT, value, location), result.location)

    def _get_literal_string_token(self, location: Location, current: Some):
        """Retrieves a literal string token"""
        end_term = self._any_until(current.value, current.location)
        if not isinstance(end_term, Some):
            return None
        term_loc = self._skip_char(current.value, end_term.location)
        if not isinstance(term_loc, Some):
            return Some(Token(ERROR, "Missing string terminator.", end_term.location), end_term.location)
        return Some(Token(STRING, self._convert_to_string(end_term.value), location), term_loc.location)

    @staticmethod
    def _get_simple_token(location: Location, current: Some):
        """Retrieves a single character token"""
        for stoken in SINGLETOKENS:
            if stoken.value == current.value:
                return Some(Token(stoken.type, current.value, location), current.location)
        return None

    def _get_comment(self, location: Location, right: Some):
        """retrieves a command token"""
        comment = self._any_until(['\r','\n'], right.location)
        result = Some(None, location)
        if isinstance(comment, Some):
            strvalue = self._convert_to_string(comment.value)
            result = Some(Token(COMMENT, strvalue, location), comment.location)
        return result

    @staticmethod
    def _get_assign_or_equal(location: Location, left: Some, right: Some):
        """Returns OP_DEFINE, OP_EQUAL or OP_ASSIGN token"""
        if right.value == ">":
            result = Some(Token(OP_DEFINE, '=>', location), right.location)
        elif right.value == "=":
            result = Some(Token(OP_EQUAL, '==', location), right.location)
        else:
            result = Some(Token(OP_ASSIGN, "=", location), left.location)
        return result

    @staticmethod
    def _get_lt_or_lte(location: Location, left: Some, right: Some):
        """returns OP_LTEQUAL or OP_LT based on the input"""
        if right.value == '=':
            result = Some(Token(OP_LTEQUAL, '==', location), right.location)
        else:
            result = Some(Token(OP_LT, '<', location), left.location)
        return result

    @staticmethod
    def _get_gt_or_gte(location: Location, left: Some, right: Some):
        """returns OP_GTEQUAL or OP_GT based on the input"""
        if right.value == '=':
            result = Some(Token(OP_GTEQUAL, '==', location), right.location)
        else:
            result = Some(Token(OP_GT, '>', location), left.location)
        return result

    @staticmethod
    def _get_not_or_ne(location: Location, left: Some, right: Some):
        """returns OP_NOTEQUAL or OP_NOT based on the input"""
        if right.value == '=':
            result = Some(Token(OP_NOTEQUAL, '!=', location), right.location)
        else:
            result = Some(Token(OP_NOT, '!', location), left.location)
        return result

    def _get_extended_token(self, location: Location, left: Some):
        """Retrieves a token that is made up from either one or two characters
           that have a specific meaning, like equality and assignment == and ="""
        right = self._get_current_char(left.location)
        if not isinstance(right, Some):
            right = Some(None, left.location)
        result = None
        if left.value == "=":
            result = self._get_assign_or_equal(location, left, right)
        elif left.value == '<':
            result = self._get_lt_or_lte(location, left, right)
        elif left.value == '>':
            result = self._get_gt_or_gte(location, left, right)
        elif left.value == '!':
            result = self._get_not_or_ne(location, left, right)
        elif left.value == '/' and right.value == "/":
            result = self._get_comment(location, right)
        elif left.value == '/':
            result = Some(Token(OP_DIV, left.value, left.location), left.location)
        return result

    def _lex(self, location: Location):
        """Scans the source for the next token and returns it. Returns None if end of
        source or unknown"""
        next_loc = self._skip_whitespace(location)
        current = self._get_current_char(next_loc)
        if not isinstance(current, Some):
            token = Some(None, next_loc)
        elif current.value.isalpha():
            token = self._get_identifier(next_loc, current)
        elif current.value.isdigit():
            token = self._get_literal_number_token(next_loc)
        elif current.value == '"' or current.value == '\'':
            token = self._get_literal_string_token(next_loc, current)
        else:
            token = self._get_simple_token(location, current)
            if token is None:
                token = self._get_extended_token(location, current)
        if not isinstance(token, Some):
            return Some(None, next_loc)
        return token

    def lex_line(self, source: str, line: int):
        """Initializes source and scans it for tokens, returns a list of tokens found.
        Returns None if source is empty or None."""
        if source is None:
            return None
        self.source = source
        self.length = len(source)
        if self.length == 0:
            return None
        lst = []
        location = Location(0, line, 0)
        some = self._lex(location)
        while isinstance(some.value, Token):
            lst.append(some.value)
            location = some.location
            some = self._lex(location)
        
        #detect eof
        if some.value is None and some.location.pos >= self.length:
            return lst
        # Perhaps an error, but it may still be legit for exitting before eof.
        if location.pos < self.length-1:
            peek = self._get_current_char(location)
            if isinstance(peek, Some):
                lst.append(Token(ERROR, "Unknown character '{}'".format(peek.value), location))
        return lst

    def lex(self, source: str):
        """Initializes source code and scans all tokens in the source"""
        tokens = self.lex_line(source, 0)
        return tokens
