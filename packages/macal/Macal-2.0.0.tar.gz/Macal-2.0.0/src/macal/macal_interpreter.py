#-------------------------------------------------------------------------------------------------#
# Filename:       | macal_interpreter.py                                                          #
# Author:         | Marco Caspers                                                                 #
# Description:    |                                                                               #
#-------------------------------------------------------------------------------------------------#
#                                                                                                 #
# Macal 2.0 Interpreter class                                                                     #
#                                                                                                 #
###################################################################################################

"""macal Language Interpreter class implementation"""

from .macal_parsernodetypes import (BLOCK, ASSIGN, ELSE, FUNCTION, CALL, FOREACH, HALT, BREAK, 
                                   RETURN, SELECT, IF)
from .macal_lextokentypes import NEW_ARRAY_INDEX
from .macal_variable_types import ANY, ARRAY, BOOL, FLOAT, INT, PARAMS, STRING, RECORD
from .macal_parsernodetypes import VARIABLE
from .macal_keywords import NIL
from .macal_exprtypes import LITERAL, BINARY, UNARY, GROUPING, FUNCTION
from .macal_interpreterconsts import EXIT_VAR_NAME, SelectFieldFilter

from .macal_variable import PVariable
from .macal_function import PFunction
from .macal_parsernodes import ast_Break, ast_Variable, ast_Function_definition, ast_list_Index
from .macal_astifnode import ast_If
from .macal_expritem import ExpressionItem
from .macal_astselectnode import ast_Select

from .macal_expr import Expr
from .macal_scope import PScope

#from decimal import Decimal

class PInterpreter:
    def __init__(self):
        self.ast_tree = None
        self.scope = PScope("root", None)
        self.version = "2.0"

    @staticmethod
    def raise_error(message: str, instruction, scope: PScope):
        raise Exception("Runtime error: {} \nScope: {}\n{}".format(message, scope.name, instruction))

    def interpret(self, ast_tree):
        var = self.scope.find_variable(EXIT_VAR_NAME)
        if var is None:
            var = self.scope.add_new_variable(EXIT_VAR_NAME)
        var.set_value(0)
        var.set_type(INT)
        self.ast_tree = ast_tree
        self.interpret_block(self.ast_tree, self.scope)
        return var.get_value()

    def interpret_instruction(self, instruction, scope: PScope):
        if instruction.type == ASSIGN:
            self.interpret_assign(instruction, scope)
        elif instruction.type == BLOCK:
            self.interpret_block(instruction, scope)
        elif instruction.type == BREAK:
            self.interpret_break_loop(instruction, scope)
        elif instruction.type == CALL:
            self.interpret_function_call(instruction, scope)
        elif instruction.type == FOREACH:
            self.interpret_foreach_loop(instruction, scope)
        elif instruction.type == FUNCTION:
            self.interpret_function_definition(instruction, scope)
        elif instruction.type == HALT:
            self.interpret_halt(instruction, scope)
        elif instruction.type == RETURN:
            self.interpret_return(instruction, scope)
        elif instruction.type == IF:
            self.interpret_if(instruction, scope)
        elif instruction.type == SELECT:
            self.interpret_select(instruction, scope)
        else:
            self.raise_error("Unknown instruction", instruction, scope)

    def evaluate_expression(self, expr, scope: PScope):
        if isinstance(expr, ast_Variable):
            return self._eval_var(expr, scope)
        elif isinstance(expr, PVariable):
            return self._eval_variable(expr, scope)
        elif isinstance(expr, ast_list_Index):
            return self._eval_index(expr, scope)
        elif expr.expr_type == LITERAL:
            return ExpressionItem(expr.left.value, expr.left.item_type)
        elif expr.expr_type == BINARY:
            return self._eval_binary_expr(expr, scope)
        elif expr.expr_type == UNARY:
            return self._eval_unary_expr(expr, scope)
        elif expr.expr_type == GROUPING:
            return self._eval_grouping_expr(expr, scope)
        elif expr.expr_type == FUNCTION:
            return self._eval_function_expr(expr, scope)
        self.raise_error("Unknown expression type ({})".format(expr.expr_type), expr, scope)

    def _eval(self, expr: ExpressionItem, scope: PScope):
        if isinstance(expr.value, ast_Variable):
            return self._eval_var(expr.value, scope)
        elif isinstance(expr.value, Expr):
            result = self.evaluate_expression(expr.value, scope)
            return result
        self.raise_error("Unknown instance ({})".format(type(expr.value)), expr, scope)

    def _eval_var(self, expr: ast_Variable, scope: PScope):
        var = scope.find_variable(expr.name())
        if var is None:
            var = scope.find_function(expr.name())
            if var is None:
                self.raise_error("Variable not found {}".format(expr.name()), expr, scope)
            else:
                return ExpressionItem(var, FUNCTION)
        if expr.has_index():
            index = []
            for index_expr in expr.index:
                iev = self.evaluate_expression(index_expr, scope)
                index.append(iev)
            return self._eval_indexed_var(var, index, scope)
        return ExpressionItem(var.get_value(), var.get_type())

    def _eval_indexed_var(self, var: PVariable, index: list, scope: PScope):
        value = var.get_value()
        for idx in index:
            if isinstance(value, dict) and not idx.value in value:
                self.raise_error("Index not found: {} ({})".format(idx.value, var.name), idx, scope)
            elif isinstance(value, list)  and not 0 <= idx.value < len(value):
                self.raise_error("Index not found: {} ({})".format(idx.value, var.name), idx, scope)
            elif not (isinstance(value, dict) or isinstance(value, list)):
                self.raise_error("Index not valid?: {} ({})".format(value, var.name), idx, scope)
            value = value[idx.value]
                    
        return ExpressionItem(value, scope.get_value_type(value))
    
    def _eval_index(self, index: ast_list_Index, scope: PScope):
        result = self.evaluate_expression(index.expr, scope)
        return result

    def _eval_variable(self, var: PVariable, scope: PScope):
        return ExpressionItem(var.get_value(), var.get_type())

    def _eval_binary_expr(self, expr: Expr, scope: PScope):
        left  = self._eval(expr.left, scope)
        right = self._eval(expr.right, scope)
        result_type = left.item_type
        if left.item_type == INT and right.item_type == FLOAT or left.item_type == FLOAT and right.item_type == INT:
            #if isinstance(left.value, int) or isinstance(left.value, float):
            #left.value = Decimal(left.value)
            #right.value = Decimal(right.value)
            result_type = FLOAT
        elif left.item_type != right.item_type:
            self.raise_error("Incompatible operand types {},{}".format(left.item_type, right.item_type), expr, scope)
        if left.value is None or right.value is None:
            return
        if expr.operator == '>':
            return ExpressionItem(left.value > right.value, BOOL)
        elif expr.operator == '<':
            return ExpressionItem(left.value < right.value, BOOL)
        elif expr.operator == '>=':
            return ExpressionItem(left.value >= right.value, BOOL)
        elif expr.operator == '<=':
            return ExpressionItem(left.value >= right.value, BOOL)
        elif expr.operator == '==':
            return ExpressionItem(left.value == right.value, BOOL)
        elif expr.operator == '*':
            return ExpressionItem(left.value * right.value, result_type)
        elif expr.operator == '/':
            if right.value == 0 or right.value == 0.0:
                self.raise_error("Division by zero.", expr, scope)
            return ExpressionItem(left.value / right.value, result_type)
        elif expr.operator == '+':
            return ExpressionItem(left.value + right.value, result_type)
        elif expr.operator == '-':
            return ExpressionItem(left.value - right.value, result_type)

        self.raise_error("Unknown op in expression ({})".format(expr.operator), expr, scope)

    def _eval_unary_expr(self, expr: Expr, scope: PScope):
        right = self._eval(expr.right, scope)
        # neg
        if expr.operator == '-' and (right.item_type == INT or right.item_type == FLOAT):
            return ExpressionItem(right.value * -1, right.item_type)
        # not
        elif expr.operator == '!' and right.item_type == BOOL:
            return ExpressionItem(not right.value, BOOL)
        elif expr.operator == '&' or expr.operator == '$':
            return right
        self.raise_error("Incompatible type: ({})".format(right.item_type), expr, scope)
    
    def _eval_grouping_expr(self, expr: Expr, scope: PScope):
        return self._eval(expr.left, scope)
    
    def _eval_function_expr(self, expr: Expr, scope:PScope):
        fval = self.interpret_function_call(expr.left.value, scope)
        while not isinstance(fval, ExpressionItem):
            fval = self.evaluate_expression(fval, scope)
        return fval

    def interpret_assign(self, instruction, scope: PScope):
        if instruction.expr is None:
            self.raise_error("Expression is None", instruction, scope)
        if instruction.ident.has_index():
            self._interpret_indexed_assign(instruction, scope)
            return
        var_name = instruction.ident.name()
        var = scope.find_variable(var_name)
        if var is None:
            var = scope.add_new_variable(var_name)
        
        item = self.evaluate_expression(instruction.expr, scope)
        var.set_type(item.item_type)
        var.set_value(item.value)

    def _interpret_indexed_assign(self, instruction, scope: PScope):
        var_name = instruction.ident.name()
        var = scope.find_variable(var_name)
        if var is None:
            self.raise_error("Variable not found: {}".format(var_name), instruction, scope)
        var_type = var.get_type()
        var_value = var.get_value()
        if not (var_type == ARRAY or var_type == RECORD):
            self.raise_error("Incompatible variable type: {}".format(var_type), instruction, scope)
        index = []
        index_value = var_value
        count = len(instruction.ident.index)
        iind = 0
        for idx in instruction.ident.index:
            if not (isinstance(index_value, list) or isinstance(index_value, dict)):
                self.raise_error("Indexed value is not an array: {}[] {}".format(var_name, index_value), instruction, scope)
            max_idx = len(index_value)
            
            idv = self.evaluate_expression(idx.expr,scope)
            if idv.item_type == ARRAY and idv.value == NEW_ARRAY_INDEX:
                index.append(idv.value)
                break
            if idv.item_type == STRING and not isinstance(index_value, dict):
                self.raise_error("Not a record {}..[{}]".format(var_name, var_type), instruction, scope)
            elif not isinstance(index_value, dict) and (idv.item_type != INT or not isinstance(idv.value, int)):
                self.raise_error("Invalid index value {}..[{}]".format(var_name, idv.item_type), instruction, scope)
            if isinstance(index_value, list) and idv.value >= max_idx:
                self.raise_error("Variable index out of range: {}..[{}]".format(var_name, idv.value), instruction, scope)
            index.append(idv.value)
            if var_type == RECORD and isinstance(index_value, dict) and idv.value not in index_value:
                index_value[idv.value] = None
                break
            if iind < count - 1:
                if isinstance(index_value, list) and isinstance(idv.value, int):
                    if index_value[idv.value] is not None:
                        index_value = index_value[idv.value]
                elif isinstance(index_value, dict):
                    if index_value[idv.value] is not None:
                        index_value = index_value[idv.value]
            iind += 1
        item = self.evaluate_expression(instruction.expr, scope)
        if index[iind-1] != NEW_ARRAY_INDEX:
            index_value[index[iind-1]] = item.value
        elif isinstance(index_value, list):
            index_value.append(item.value)
        else:
            self.raise_error("Invalid new array index on record.", instruction, scope)

    def interpret_block(self, block, scope: PScope):
        for instruction in block.instruction_list:
            self.interpret_instruction(instruction, scope)
            if scope.break_flag or scope.get_halt():
                break

    def interpret_break_loop(self, instruction, scope: PScope):
        if scope.is_loop:
            scope.break_flag = True
        else:
            self.raise_error("not in loop", scope, instruction)

    def interpret_function_call(self, instruction, scope: PScope):
        func = scope.find_function(instruction.name())
        if func is None:
            var = scope.find_variable(instruction.name())
            if var is not None:
                value = var.get_value()
                if (isinstance(value, PFunction)):
                    func = value
                else:
                    self.raise_error("function not found: {}".format(instruction.name()), instruction, scope)
            else:
                self.raise_error("function not found: {}".format(instruction.name()), instruction, scope)
                
        call_scope = scope.create_child('call {}'.format(instruction.name()))
        return_var = call_scope.add_new_variable('?return_var{}'.format(call_scope.name))
        return_var.set_type(NIL)
        return_var.set_value(NIL)
        param_list = []
        if func.parameters.count() == 1 and func.parameters.params[0].token.type == PARAMS:
            index = 0
            for expr in instruction.params.params:
                pn = f"{func.parameters.params[0].name()}{index}"
                index += 1
                var = call_scope.add_new_variable(pn)
                param_list.append(var)
                value = self.evaluate_expression(expr, scope)
                if (isinstance(value, ExpressionItem)):
                    var.set_value(value.value)
                    var.set_type(value.item_type)
                else:
                    self.raise_error("Unknown return type", value, scope)
        else:
            for param, instr in zip(func.parameters.params, instruction.params.params):
                var = call_scope.add_new_variable(param.name())
                param_list.append(var)
                value = None
                if param.token.type == VARIABLE:
                    value = ExpressionItem(instr.token.value, VARIABLE)
                else:
                    value = self.evaluate_expression(instr, scope)
                if (isinstance(value, ExpressionItem)):
                    var.set_value(value.value)
                    var.set_type(value.item_type)
                else:
                    self.raise_error("Unknown return type", value, scope)
                
        if func.is_extern:
            func.call_extern(func, instruction.name(), param_list, call_scope)
        else:
            self.interpret_block(func.block, call_scope)
        #scope.remove_child(call_scope) #for testing purposes we don't remove the child scope.
        return return_var

    def interpret_foreach_loop(self, instruction, scope: PScope):
        loop_var   = scope.find_variable(instruction.expr.name())
        if loop_var is None:
            self.raise_error("Foreach variable not found.", instruction.expr.name(), scope)
        loop_scope = scope.create_child("foreach")
        foreach_var = loop_scope.add_new_variable('it')
        foreach_var.set_type(ANY)
        foreach_var.set_value(None)
        walker = loop_var.get_value()
        for value in walker:
            foreach_var.set_value(value)
            self.interpret_block(instruction.block, loop_scope)
            if loop_scope.break_flag or loop_scope.get_halt():
                break;

    def interpret_function_definition(self, instruction: ast_Function_definition, scope: PScope):
        func = scope.find_function(instruction.name())
        if func is not None:
            self.raise_error("function already exists", instruction, scope)
        scope.add_new_function(instruction.name(), instruction.params, instruction.block)

    def interpret_halt(self, instruction, scope: PScope):
        exit_var = self.scope.find_variable(EXIT_VAR_NAME)
        if exit_var is None:
            exit_var = self.scope.add_new_variable(EXIT_VAR_NAME)
        value = self.evaluate_expression(instruction.expr, scope);
        exit_var.set_type(value.item_type)
        exit_var.set_value(value.value)
        scope.set_halt()
        self._walk_scopes_terminate(self.scope)

    def interpret_return(self, instruction, scope: PScope):
        exit_var = scope.find_variable("?return_var{}".format(scope.name))
        if exit_var is None:
            self.raise_error("Not in a function?", instruction, scope)
        value = self.evaluate_expression(instruction.expr, scope);
        exit_var.set_type(value.item_type)
        exit_var.set_value(value.value)
        scope.break_flag = True

    def interpret_if(self, instruction: ast_If, scope: PScope):
        flag = False
        if self.evaluate_expression(instruction.condition, scope).value:
            if_scope = instruction.scope    # re-use the scope that exists to prevent dozens of being created if in a loop.
            if if_scope is None:
                if_scope = scope.create_child("if")
                instruction.scope = if_scope
            self.interpret_block(instruction.block,if_scope)
            flag = True
        if not flag and instruction.has_elif():
            branch_index = 0
            for branch in instruction.elif_branch:
                if self.evaluate_expression(branch.condition, scope).value:
                    branch_scope = branch.scope
                    if branch_scope is None:
                        branch_scope = scope.create_child("elif{}".format(branch_index))
                        branch.scope = branch_scope
                    self.interpret_block(branch.block, branch_scope)
                    flag = True
                    break
                branch_index += 1
        if not flag and instruction.has_else():
            branch_scope = instruction.else_branch.scope
            if branch_scope is None:
                branch_scope = scope.create_child("else")
                instruction.else_branch.scope = branch_scope
            self.interpret_block(instruction.else_branch.block, branch_scope)
    
    def _walk_scopes_terminate(self, scope: PScope):
        for child in scope.children:
            child.halt_flag = True
            if (len(child.children) > 0):
                self._walk_scopes_terminate(child)
                
    def interpret_select(self, instruction: ast_Select, scope: PScope):
        from_expr = instruction.sfrom
        source_data = self.evaluate_expression(from_expr, scope).value
        if not (isinstance(source_data, list) or isinstance(source_data, dict)):
            self.raise_error("Select from needs to be a record or an array of records", from_expr, scope)
        if isinstance(source_data, dict):
            source_data = [source_data]
        into_expr = instruction.into
        if not isinstance(into_expr, ast_Variable):
            self.raise_error("Select Into must be a variable.", into_expr, scope)
        into = into_expr.name()
        destination = scope.find_variable(into);
        # select will always return an array of records
        # so here we ensure that this is always the case regardless of the destination existing or not.
        destination_data = []
        if destination is None:
            destination = scope.add_new_variable(into)
            destination.set_value(destination_data)
        else:
            destination_data = destination.get_value()
            if not (isinstance(destination_data, list) or isinstance(destination_data, dict)) and instruction.merge:
                self.raise_error("Select into variable needs to be an array or a record.", into_expr, scope)
            elif isinstance(destination_data, dict) and instruction.merge:
                destination_data = [destination_data]
                destination.set_value(destination_data)
            else: # we reset to a blank array if data does not need to be merged.
                destination.set_value(destination_data)
        destination.set_type(ARRAY)
        field_filters = []
        # params is of type SelectParam.
        # This is a named tuple that has 3 elements:
        # - token       This is the lexer token that has the name of the field to filter on as its value.
        # - astoken     This is an optional token that contains the lexer token for the AS 
        # - asvalue
        for param in instruction.params:
            field_name = param.token.value
            as_name = field_name
            if param.asvalue is not None:
                as_name = param.asvalue.value
            field_filters.append(SelectFieldFilter(field_name, as_name))
        if not isinstance(destination_data, list):
            self.raise_error("Invalid destination data type.", into_expr, scope)
        if len(field_filters) == 1 and field_filters[0].field_name == '*':
            for record in source_data:
                if self._evaluate_data_filter(instruction.where, record, scope):
                    destination_data.append(record)
            destination.set_value(destination_data)
        else:
            for record in source_data:
                if self._evaluate_data_filter(instruction.where, record, scope):
                    destination_record = self.apply_field_filter(record, field_filters, into_expr,  scope)
                    destination_data.append(destination_record)
            destination.set_value(destination_data)

    def apply_field_filter(self, record, field_filters, expr, scope: PScope):
        destination_record = dict()
        for field_filter in field_filters:
            src_field = field_filter.field_name
            dst_field = field_filter.as_name
            if not src_field in record:
                self.raise_error("Field not found: {}".format(src_field), expr, scope)
            destination_record[dst_field] = record[src_field]
        return destination_record

    def _evaluate_data_filter(self, where, record: dict, scope: PScope):
        if where is None:
            return True
        value = self.evaluate_df(where, record, scope)
        return value.item_type == BOOL and value.value
    
    @staticmethod
    def raise_df_error(message: str):
        raise Exception(message)
    
    def evaluate_df(self, expr, record: dict, scope: PScope):
        if isinstance(expr, ast_Variable):
            return self._eval_var_df(expr, record, scope)
        elif isinstance(expr, PVariable):
            return self._eval_variable_df(expr, record, scope)
        elif isinstance(expr, ast_list_Index):
            return self._eval_index_df(expr, record, scope)
        elif expr.expr_type == LITERAL:
            return ExpressionItem(expr.left.value, expr.left.item_type)
        elif expr.expr_type == BINARY:
            return self._eval_binary_df(expr, record, scope)
        elif expr.expr_type == UNARY:
            return self._eval_unary_df(expr, record, scope)
        elif expr.expr_type == GROUPING:
            return self._eval_grouping_df(expr, record, scope)
        elif expr.expr_type == FUNCTION:
            return self._eval_function_df(expr, record, scope)
        self.raise_df_error("Unknown expression type ({})".format(expr.expr_type))
        #self.raise_error("Unknown expression type ({})".format(expr.expr_type), expr, record)

    def _eval_df(self, expr: ExpressionItem, record: dict, scope: PScope):
        if isinstance(expr.value, ast_Variable):
            return self._eval_var_df(expr.value, record, scope)
        elif isinstance(expr.value, Expr):
            result = self.evaluate_df(expr.value, record, scope)
            return result
        self.raise_df_error("Unknown instance ({})".format(type(expr.value)))
        #self.raise_error("Unknown instance ({})".format(type(expr.value)), expr, record)

    def _get_var_df(self, expr: ast_Variable, record: dict, scope: PScope):
        var = scope.find_variable(expr.name())
        if var is None:
            self.raise_error("Variable not found {}".format(expr.name()), expr, scope)
        if expr.has_index():
            index = []
            for index_expr in expr.index:
                iev = self.evaluate_expression(index_expr, scope)
                index.append(iev)
            return self._eval_indexed_var(var, index, scope)
        return ExpressionItem(var.get_value(), var.get_type())

    def _eval_var_df(self, expr: ast_Variable, record: dict, scope: PScope):
        if not expr.name() in record:
            var = scope.find_variable(expr.name())
            if var is None:
                self.raise_df_error("Field not found: {} {}".format(expr.name(), record))
            return self._get_var_df(expr, record, scope)

        var = record[expr.name()]
        return ExpressionItem(var, scope.get_value_type(var))
    
    def _eval_indexed_var_df(self, var: PVariable, index: list, record: dict, scope: PScope):
        value = var.get_value()
        for idx in index:
            if isinstance(value, dict) and not idx.value in value:
                self.raise_error("Index not found: {} ({})".format(idx.value, var.name), idx, scope)
            elif isinstance(value, list)  and not 0 <= idx.value < len(value):
                self.raise_error("Index not found: {} ({})".format(idx.value, var.name), idx, scope)
            elif not (isinstance(value, dict) or isinstance(value, list)):
                self.raise_error("Index not valid?: {} ({})".format(value, var.name), idx, scope)
            value = value[idx.value]
                    
        return ExpressionItem(value, scope.get_value_type(value))
    
    def _eval_index_df(self, index: ast_list_Index, record: dict, scope: PScope):
        result = self.evaluate_df(index.expr, record, scope)
        return result

    def _eval_variable_df(self, var: PVariable, record: dict, scope: PScope):
        return ExpressionItem(var.get_value(), var.get_type())

    def _eval_binary_df(self, expr: Expr, record: dict, scope: PScope):
        left  = self._eval_df(expr.left, record, scope)
        right = self._eval_df(expr.right, record, scope)
        result_type = left.item_type
        if left.item_type == INT and right.item_type == FLOAT or left.item_type == FLOAT and right.item_type == INT:
            result_type = FLOAT
        elif left.item_type != right.item_type:
            self.raise_error("Incompatible operand types {},{}".format(left.item_type, right.item_type), expr, scope)
        if left.value is None or right.value is None:
            return
        if expr.operator == '>':
            return ExpressionItem(left.value > right.value, BOOL)
        elif expr.operator == '<':
            return ExpressionItem(left.value < right.value, BOOL)
        elif expr.operator == '>=':
            return ExpressionItem(left.value >= right.value, BOOL)
        elif expr.operator == '<=':
            return ExpressionItem(left.value >= right.value, BOOL)
        elif expr.operator == '==':
            return ExpressionItem(left.value == right.value, BOOL)
        elif expr.operator == '*':
            return ExpressionItem(left.value * right.value, result_type)
        elif expr.operator == '/':
            if right.value == 0 or right.value == 0.0:
                self.raise_error("Division by zero.", expr, scope)
            return ExpressionItem(left.value / right.value, result_type)
        elif expr.operator == '+':
            return ExpressionItem(left.value + right.value, result_type)
        elif expr.operator == '-':
            return ExpressionItem(left.value - right.value, result_type)

        self.raise_error("Unknown op in expression ({})".format(expr.operator), expr, scope)

    def _eval_unary_df(self, expr: Expr, record: dict, scope: PScope):
        right = self._eval(expr.right, scope)
        # neg
        if expr.operator == '-' and (right.item_type == INT or right.item_type == FLOAT):
            return ExpressionItem(right.value * -1, right.item_type)
        # not
        elif expr.operator == '!' and right.item_type == BOOL:
            return ExpressionItem(not right.value, BOOL)
        elif expr.operator == '&' or expr.operator == '$':
            return right
        self.raise_error("Incompatible type: ({})".format(right.item_type), expr, scope)
    
    def _eval_grouping_df(self, expr: Expr, record: dict, scope: PScope):
        return self._eval_df(expr.left, record, scope)
    
    def _eval_function_df(self, expr: Expr, record: dict, scope:PScope):
        fval = self.interpret_function_call(expr.left.value, scope)
        while not isinstance(fval, ExpressionItem):
            fval = self.evaluate_expression(fval, scope)
        return fval
