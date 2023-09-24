from collections import defaultdict
from grin import parse, GrinTokenKind
from help import GrinRuntimeException
class Program:

    std = [GrinTokenKind.INSTR, GrinTokenKind.INNUM, GrinTokenKind.PRINT]
    operation = [GrinTokenKind.ADD, GrinTokenKind.SUB,GrinTokenKind.MULT,GrinTokenKind.DIV,GrinTokenKind.LET]
    branch = [GrinTokenKind.GOTO,GrinTokenKind.GOSUB]
    back = GrinTokenKind.RETURN
    def __init__(self):
        self.program = []
        self.counter = 0
        self.functions = {}
        self.raw = []
        self.stack = []
        self.variables = defaultdict(int)

    def add_raw(self,statement):
        self.raw.append(statement)

    def preprocess(self):
        self.program = list(parse(self.raw))
        for i in range(len(self.program)):
            row = self.program[i]
            first_token = row[0]

            if first_token.kind() == GrinTokenKind.IDENTIFIER:
                self.functions[first_token.text()] = first_token.location().line() - 1
                self.program[i]= row[2:]

    def io(self,command, token):
        if command == GrinTokenKind.PRINT:
            self.std_out(token)
        else:
            self.std_in(command,token)
    def std_in(self,command, token):
        val = input()
        if command == GrinTokenKind.INSTR:
            self.variables[token.value()] = val
        else:
            if '.' in val:
                try:
                    self.variables[token.value()] = float(val)
                except ValueError as e:
                    raise GrinRuntimeException("invalid float from input", token.location())
            else:
                self.variables[token.value()] = int(val)

    def end(self):
        self.counter = len(self.program)

    def forward(self):
        self.counter +=1

    def runnable(self):
        # print('counter',self.counter)
        # print('len',len(self.program))
        return self.counter < len(self.program)

    def jump(self, keyword_kind, target, location):
        msg = 'GOTO' if keyword_kind == GrinTokenKind.GOTO else 'GOSUB'
        if keyword_kind == GrinTokenKind.GOSUB:
            if target.kind() == GrinTokenKind.LITERAL_INTEGER:
                if target.value() == 0 or target.value() + self.counter < 0 or target.value() + self.counter >= len(
                        self.program):
                    raise GrinRuntimeException(f'invalid {msg} statement', location)

                self.stack.append(self.counter+1)
                self.counter = target.value() + self.counter
            elif target.kind() == GrinTokenKind.LITERAL_STRING:
                if self.functions.get(target.value()) is None:
                    # print(self.functions, target.text())
                    # print(self.functions.get(target.text()))
                    raise GrinRuntimeException(f'invalid {msg} statement', location)

                self.stack.append(self.counter + 1)
                self.counter = self.functions.get(target.value())
            else:
                if self.functions.get(target.text()) is None:
                    # print(self.functions, target.text())
                    # print(self.functions.get(target.text()))
                    raise GrinRuntimeException(f'invalid {msg} statement', location)

                self.stack.append(self.counter + 1)
                self.counter = self.functions.get(target.text())
        elif keyword_kind == GrinTokenKind.GOTO:
            if target.kind() == GrinTokenKind.LITERAL_INTEGER:
                if target.value() == 0 or target.value() + self.counter < 0 or target.value() + self.counter >= len(self.program):
                    raise GrinRuntimeException(f'invalid {msg} statement',location)

                self.counter = target.value() + self.counter
            elif target.kind() == GrinTokenKind.LITERAL_STRING:
                if self.functions.get(target.value()) is None:
                    raise GrinRuntimeException(f'invalid {msg} statement',location)
                else:
                    self.counter = self.functions.get(target.value())
            else:
                if self.functions.get(target.text()) is None:
                    raise GrinRuntimeException(f'invalid {msg} statement',location)
                else:
                    self.counter = self.functions.get(target.text())

    def backtrack(self):
        self.counter = self.stack.pop() if len(self.stack) > 0 else self.counter+1

    def eval(self, op1, comp_kind, op2, location):
        val1 = self.variables[op1.text()] if op1.kind() == GrinTokenKind.IDENTIFIER else op1.value()
        val2 = self.variables[op2.text()] if op2.kind() == GrinTokenKind.IDENTIFIER else op2.value()
        if (type(val1) is str and type(val2) is not str) or (type(val1) is not str and type(val2) is str):
            raise GrinRuntimeException("invalid operands for comparison", location)


        if comp_kind == GrinTokenKind.LESS_THAN:
            return val1 < val2
        elif comp_kind == GrinTokenKind.LESS_THAN_OR_EQUAL:
            return val1 <= val2
        elif comp_kind == GrinTokenKind.GREATER_THAN:
            return val1 > val2
        elif comp_kind == GrinTokenKind.GREATER_THAN_OR_EQUAL:
            return val1 >= val2
        elif comp_kind == GrinTokenKind.EQUAL:
            return val1 == val2
        else:
            return val1 != val2



    def get_statement(self):
        return self.program[self.counter]
    def std_out(self, token):
        print(self.variables[token.value()]) if token.kind() == GrinTokenKind.IDENTIFIER else print(token.value())


    def op(self,kind,op1,op2):
        if kind == GrinTokenKind.LET:
            self.let(op1,op2)
        elif kind == GrinTokenKind.ADD:
            self.add(op1,op2)
        elif kind == GrinTokenKind.SUB:
            self.sub(op1,op2)
        elif kind == GrinTokenKind.MULT:
            self.mult(op1,op2)
        else:
            self.div(op1,op2)

    def let(self,op1,op2):
        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.variables[op1.text()] = self.variables[op2.text()]
        else:
            self.variables[op1.text()] = op2.value()

    def add(self,op1,op2):
        if type(self.variables[op1.text()]) is str:
            if type(op2.value()) is int or type(op2.value()) is float \
                    or (op2.kind() is GrinTokenKind.IDENTIFIER and type(self.variables[op2.text()]) is int) \
                    or (op2.kind() is GrinTokenKind.IDENTIFIER and type(self.variables[op2.text()]) is float):
                raise GrinRuntimeException("can't add number and string", op1.location())
        else:
            if type(op2.value()) is str or \
                    type(self.variables[op2.text()]) is str:
                raise GrinRuntimeException("can't add number and string", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.variables[op1.text()] += self.variables[op2.text()]
        else:
            self.variables[op1.text()] += op2.value()

    def sub(self,op1,op2):
        if type(self.variables[op1.text()]) is str or\
            op2.value() is str or (op2.kind() == GrinTokenKind.IDENTIFIER and type(self.variables[op2.text()]) is str):
            raise GrinRuntimeException("can't subtract string", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.variables[op1.text()] -= self.variables[op2.text()]
        else:
            self.variables[op1.text()] -= op2.value()

    def mult(self,op1,op2):
        if type(self.variables[op1.text()]) is str and\
            (type(op2.value()) is str or (op2.kind() == GrinTokenKind.IDENTIFIER and type(self.variables[op2.text()]) is str)):
            raise GrinRuntimeException("can't multiply two strings", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.variables[op1.text()] *= self.variables[op2.text()]
        else:
            self.variables[op1.text()] *= op2.value()

    def div(self,op1,op2):
        if type(self.variables[op1.text()]) is str or\
            type(op2.value()) is str or (op2.kind() == GrinTokenKind.IDENTIFIER and type(self.variables[op2.text()]) is str):
            raise GrinRuntimeException("can't divide string", op1.location())

        if op2.value() == 0 or (op2.kind() == GrinTokenKind.IDENTIFIER and self.variables[op2.text()] == 0):
            raise GrinRuntimeException("zero operand", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            if type(self.variables[op2.text()]) is int and type(self.variables[op1.text()]) is int:
                self.variables[op1.text()] //= self.variables[op2.text()]
            else:
                self.variables[op1.text()] /= self.variables[op2.text()]
        else:
            if type(op2.value()) is int and type(self.variables[op1.text()]) is int:
                self.variables[op1.text()] //= op2.value()
            else:
                self.variables[op1.text()] /= op2.value()