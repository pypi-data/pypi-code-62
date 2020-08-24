import csv
import os.path
from SpecularLang.SpecLangTypes import Term, Operation, Type, SpecHelper, Operator, UnaryOperation

from SpecularLang.SpecLangParser import SpecLangParser
from SpecularLang.SpecLangVisitor import SpecLangVisitor


class SpecLangWalker(SpecLangVisitor):
    def __init__(self, save_dir='', scenes=None, talkative=1):
        self.rows = []
        self.allRows = []
        self.rowNum = 0
        self.preSceneRows = []
        self.is_prescene = True
        self.save_dir = save_dir
        self.scenes = scenes
        self.talkative = talkative

    def visitChoice(self, ctx:SpecLangParser.ChoiceContext):
        choices = {}
        i = 0
        while ctx.STRING(i) is not None:
            choices["choice{}".format(i)] = str(ctx.STRING(i)).strip('"')
            i += 1
        self.add_row([self.rowNum, "Choice", choices])
        return Term(Type.ID, '${}'.format(self.rowNum - 1))

    def visitDialog(self, ctx: SpecLangParser.DialogContext):
        if ctx.emotion():
            emotion = self.visit(ctx.emotion())
            i = 4
        else:
            emotion = 'Neutral'
            i = 3
        self.add_row([self.rowNum, "Dialog", {'speaker': str(ctx.getChild(1)), 'emotion': emotion, 'text': str(ctx.getChild(i)).strip('"')}])

    def visitEmotion(self, ctx: SpecLangParser.EmotionContext):
        return ctx.getText().strip("(").strip(")").strip('"')

    def visitTerm(self, ctx: SpecLangParser.TermContext) -> Term:
        if ctx.NUMBER():
            _type = Type.NUMBER
            value = ctx.getText().strip('"')
        elif ctx.TRUE() or ctx.FALSE():
            _type = Type.BOOL
            value = ctx.getText().strip('"')
        elif ctx.STRING():
            _type = Type.STRING
            value = self.convert_to_specular_string_format(ctx.getText())
        elif ctx.ID():
            _type = Type.ID
            value = ctx.getText().strip('"')
        else:
            _type = Type.NONE
            value = ctx.getText().strip('"')
        return Term(_type, value)

    def visitAssignment(self, ctx: SpecLangParser.AssignmentContext):
        if ctx.GLOBAL():
            is_global = 'Yes'
        else:
            is_global = 'No'
        term = SpecHelper.to_term(self.visit(ctx.expression()))
        self.add_row([self.rowNum, "Assign", {'global': is_global, 'ID': str(ctx.ID()), 'type': term.type.value, 'assignment': term.value}], is_prescene=self.is_prescene)

    def visitAdd(self, ctx: SpecLangParser.AddContext):
        return self.perform_expression(ctx.expression(0), ctx.expression(1), Operator(str(ctx.getChild(1))))

    def visitMult(self, ctx: SpecLangParser.MultContext):
        return self.perform_expression(ctx.expression(0), ctx.expression(1), Operator(str(ctx.getChild(1))))

    def perform_expression(self, expression_0, expression_1, operator: Operator):
        term_0 = SpecHelper.to_term(self.visit(expression_0))
        term_1 = SpecHelper.to_term(self.visit(expression_1))
        operation = Operation(term_0, term_1, operator)
        if operation.is_either_operand_of_type_id():
            self.add_row([self.rowNum, "Expression", {'operator': operator.value, 'x': term_0.value, 'y': term_1.value}])
            return Term(Type.ID, '${}'.format(self.rowNum - 1))
        else:
            return operation.perform()

    def perform_unary_operation(self, expression, operator: Operator):
        term = SpecHelper.to_term(self.visit(expression))
        operation = UnaryOperation(self.visit(expression), operator)
        if term.type == Type.ID:
            self.add_row([self.rowNum, "Unary", {'operator': operator.value, 'x': term.value}])
            return Term(Type.ID, '${}'.format(self.rowNum - 1))
        else:
            return operation.perform()

    def visitEqual(self, ctx: SpecLangParser.EqualContext):
        return self.perform_expression(ctx.expression(0), ctx.expression(1), Operator(str(ctx.getChild(1))))

    def visitAnd(self, ctx: SpecLangParser.AndContext):
        return self.perform_expression(ctx.expression(0), ctx.expression(1), Operator(str(ctx.getChild(1))))

    def visitOr(self, ctx: SpecLangParser.OrContext):
        return self.perform_expression(ctx.expression(0), ctx.expression(1), Operator(str(ctx.getChild(1))))

    def visitUnary(self, ctx: SpecLangParser.UnaryContext):
        return self.perform_unary_operation(ctx.expression(), Operator(str(ctx.getChild(0))))

    def visitParen(self, ctx: SpecLangParser.ParenContext):
        return self.visit(ctx.expression())

    def visitScene_statement(self, ctx:SpecLangParser.Scene_statementContext):
        if self.scenes is None or str(ctx.STRING())[1:-1] in self.scenes:
            self.is_prescene = False
            self.rows = self.preSceneRows.copy()
            self.rowNum = len(self.preSceneRows)
            self.visit(ctx.block())
            self.add_row([self.rowNum, "StopScene", {}])
            self.write_rows(self.rows, str(ctx.STRING())[1:-1])
            self.rows = []
            self.rowNum = 0
            self.is_prescene = True

    def visitIfstatement(self, ctx: SpecLangParser.IfstatementContext):
        current_row = self.rowNum
        term = SpecHelper.to_term(self.visit(ctx.expression()))
#        elseifs = ctx.else_if_statement()
        elseifs = []
        else_state = ctx.else_statement()
        elses_exist = elseifs != [] or else_state is not None
        if str(term.value) == 'True':
            self.visit(ctx.block())
        elif str(term.value) == 'False' and not elses_exist:
            return
        else:
            elif_count = 0
            self.add_row([self.rowNum, "If", {'condition': term.value, 'jump': 'endIf_{}'.format(current_row) if not elses_exist else 'elseif_{}'.format(current_row)}])
            self.visit(ctx.block())
            if elses_exist:
                self.add_row([self.rowNum, "JumpToLabel", {'name': 'endIf_{}'.format(current_row)}])
                self.add_row([self.rowNum, "Label", {'name': 'elseif_{}'.format(current_row)}])
#           for elseif in elseifs:
#               elif_count += 1
#               self.visit(elseif)
            if else_state:
                #self.add_row([self.rowNum, "Label", {'name': 'endElif_{}_{}'.format(current_row, elif_count)}])
                self.visit(else_state)
            self.add_row([self.rowNum, "Label", {'name': 'endIf_{}'.format(current_row)}])

#    def visitElse_if_statement(self, ctx:SpecLangParser.Else_if_statementContext):
#        current_row = self.rowNum
#       term = self.visit(ctx.expression())
#      self.add_row([self.rowNum, "If", {'condition': term['value'], 'jump': 'endElif_{}'.format(current_row)}])
#       self.visit(ctx.block())
#       self.add_row([self.rowNum, "JumpToLabel", {'name': 'endIf_{}'.format(current_row)}])
#       self.add_row([self.rowNum, "Label", {'name': 'endElif_{}'.format(current_row)}])

    def visitElse_statement(self, ctx:SpecLangParser.Else_statementContext):
        self.visit(ctx.block())

    def visitWhileLoop(self, ctx:SpecLangParser.WhileLoopContext):
        current_row = self.rowNum
        self.add_row([self.rowNum, "Label", {'name': 'beginWhile_{}'.format(current_row)}])
        term = SpecHelper.to_term(self.visit(ctx.expression()))
        if str(term.value) == 'True':
            raise Exception("While loop around line: {} will run forever (which is not allowed)".format(current_row))
        elif str(term.value) == 'False':
            self.remove_last_row()
            return
        else:
            self.add_row([self.rowNum, "If", {'condition': term.value, 'jump': 'endWhile_{}'.format(current_row)}])
            self.visit(ctx.block())
            self.add_row([self.rowNum, "JumpToLabel", {'name': 'beginWhile_{}'.format(current_row)}])
            self.add_row([self.rowNum, "Label", {'name': 'endWhile_{}'.format(current_row)}])


# Canned for now
#    def visitDoWhileLoop(self, ctx:SpecLangParser.DoWhileLoopContext):
#        current_row = self.rowNum
#        term = self.visit(ctx.expression())
#        if term['value'] == 'True':
#            raise Exception("Do-While loop around line: {} will run forever (which is not allowed)".format(current_row))
#        elif term['value'] == 'False':
#            return
#        else:
#            self.add_row([self.rowNum, "Label", {'name': 'beginDoWhile_{}'.format(current_row)}])
#            self.visit(ctx.block())
#            self.add_row([self.rowNum, "While", {'condition': term['value'], 'jump': 'doWhile_{}'.format(current_row)}])

    def visitStage_direction(self, ctx:SpecLangParser.Stage_directionContext):
        params = {}
        i = 1
        while ctx.STRING(i) is not None:
            params["param{}".format(i)] = str(ctx.STRING(i)).strip('"')
            i += 1
        self.add_row([self.rowNum, str(ctx.STRING(0)).strip('"'), params])


# region: Utils
    def to_bool(self, string: str):
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            raise ValueError('ToBool is None!')

    def write_rows(self, rows: [], file_name: str):
        with open(os.path.join(self.save_dir, (file_name + '.csv')), 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            csv_writer.writerow(["---", "ActionName", "Params"])
            csv_writer.writerows(rows)
            if self.talkative > 0:
                print("Scene {} saved to file: {}".format(file_name, csv_file.name))

    @staticmethod
    def to_unreal_row_structure(di: {}):
        #(actor=None,characterName={},dialogueColor=(B=0,G=0,R=0,A=255))
        new_dict = "("
        for x, y in di.items():
            new_dict += '("{}","{}"),'.format(x, y)
        new_dict = new_dict.rstrip(",")
        new_dict += ")"
        return new_dict

    def convert_to_specular_string_format(self, str_to_convert: str):
        # If the string we are converting doesn't have quotes then we can just return it
        if str_to_convert[0] == '"' and str_to_convert[-1] == '"':
            return r'\"{}\"'.format(str_to_convert[1:-1])
        else:
            return r'\"{}\"'.format(str_to_convert)

    def append_to_formatted_string(self, formatted_str: str, append):
        return self.convert_to_specular_string_format(formatted_str[2:-2] + append)

    def add_row(self, row: [], is_prescene=False):
        if is_prescene:
            self.preSceneRows.append([row[0], row[1], self.to_unreal_row_structure(row[2])])
        else:
            self.rows.append([row[0], row[1], self.to_unreal_row_structure(row[2])])
        self.allRows.append([row[0], row[1], self.to_unreal_row_structure(row[2])])
        self.rowNum += 1

    def remove_last_row(self):
        self.rows.pop(-1)
        self.allRows.pop(-1)
        self.rowNum -= 1

