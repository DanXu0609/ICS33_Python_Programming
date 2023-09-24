import unittest
from context import Program
from unittest.mock import patch
from grin import GrinTokenKind, GrinToken
from help import GrinRuntimeException
class TestMyProgramContext(unittest.TestCase):

    def test_raw_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        self.assertEqual(len(program.raw),2)

    def test_preprocess_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        self.assertEqual(program.program,[])
        program.preprocess()
        self.assertNotEqual(program.program, None)
        self.assertEqual(len(program.program),2)


    def test_let_function(self):
        program = Program()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None, value = 0)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = 'B', location = None, value = 3)
        program.op(GrinTokenKind.LET, token1,token2)
        self.assertEqual(program.variables['A'], 3)
        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'C', location = None, value = 5)
        program.variables['C'] = 5
        program.op(GrinTokenKind.LET, token1,token3)
        self.assertEqual(program.variables['A'],5)

    def test_add_function(self):
        program = Program()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None, value = 5)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 3)
        program.variables['A'] = 5
        program.op(GrinTokenKind.ADD, token1,token2)
        self.assertEqual(program.variables['A'],8)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'B', location = None, value = 2.6)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None, value = 3.4)
        program.variables['B'] = 2.6
        program.op(GrinTokenKind.ADD, token3, token4)
        self.assertEqual(program.variables['B'], 6.0)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'C', location = None,
                           value = 3)
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 3.4)
        program.variables['C'] = 3
        program.op(GrinTokenKind.ADD, token5, token6)
        self.assertEqual(program.variables['C'], 6.4)

        token7 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'HELLO', location = None,
                           value = 'HELLO')
        token8 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'BOO', location = None,
                           value = 'BOO')
        program.variables['HELLO'] = 'HELLO'
        program.op(GrinTokenKind.ADD, token7, token8)
        self.assertEqual(program.variables['HELLO'], 'HELLOBOO')

        token9 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'TEST', location = None,
                           value = 'TEST')
        token10 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 3.2)
        program.variables['TEST'] = 'TSET'
        self.assertRaises(GrinRuntimeException, program.op, GrinTokenKind.ADD, token9, token10)

    def test_sub_function(self):
        program = Program()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'D', location = None, value = 3.2)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 1.1)
        program.variables['D'] = 3.2
        program.op(GrinTokenKind.SUB, token1, token2)
        self.assertEqual(program.variables['D'], 2.1)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'E', location = None,
                           value = 3)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 1.1)
        program.variables['E'] = 3
        program.op(GrinTokenKind.SUB, token3, token4)
        self.assertEqual(program.variables['E'], 1.9)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'EXAMPLE', location = None,
                           value = 'EXAMPLE')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                            value = 3.2)
        program.variables['EXAMPLE'] = 'EXAMPLE'
        self.assertRaises(GrinRuntimeException, program.op, GrinTokenKind.SUB, token5, token6)

    def test_mult_function(self):
        program = Program()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '3' , location = None,
                           value = 3)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 12.5)
        program.variables['3'] = 3
        program.op(GrinTokenKind.MULT, token1, token2)
        self.assertEqual(program.variables['3'], 37.5)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Boo', location = None,
                           value = 'Boo')
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 3)
        program.variables['Boo'] = 'Boo'
        program.op(GrinTokenKind.MULT, token3, token4)
        self.assertEqual(program.variables['Boo'], 'BooBooBoo')

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Hi', location = None,
                           value = 'Hi')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'World', location = None,
                           value = 'World')
        program.variables['Hi'] = 'Hi'
        self.assertRaises(GrinRuntimeException, program.op, GrinTokenKind.MULT, token5, token6)

    def test_div_function(self):
        program = Program()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '7', location = None,
                           value = 7 )
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        program.variables['7'] = 7
        program.op(GrinTokenKind.DIV, token1, token2)
        self.assertEqual(program.variables['7'], 3)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '9', location = None,
                           value = 9)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 2.0)
        program.variables['9'] = 9
        program.op(GrinTokenKind.DIV, token3, token4)
        self.assertEqual(program.variables['9'], 4.5)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Good', location = None,
                           value = 'Good')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'Job', location = None,
                           value = 'Job')
        program.variables['Good'] = 'Good'
        self.assertRaises(GrinRuntimeException, program.op, GrinTokenKind.DIV, token5, token6)

    def test_runnable_function(self):
        program = Program()
        self.assertFalse(program.runnable())
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        program.preprocess()
        self.assertTrue(program.runnable())

    def test_forword_function(self):
        program = Program()
        program.forward()
        self.assertEqual(program.counter,1)

    def test_end_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        program.preprocess()
        program.end()
        self.assertEqual(program.counter, len(program.program))
        self.assertFalse(program.runnable())

    def test_eval_function(self):
        program = Program()
        token1 =  GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '9', location = None,
                           value = 9)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 2.0)
        token3 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'Job', location = None,
                           value = 'Job')

        program.variables['9'] = 9
        program.variables['Job'] = 'Job'

        self.assertTrue(program.eval(token1, GrinTokenKind.GREATER_THAN,token2,None))
        self.assertTrue(program.eval(token1, GrinTokenKind.GREATER_THAN_OR_EQUAL, token2,None))
        self.assertFalse(program.eval(token1, GrinTokenKind.LESS_THAN, token2,None))
        self.assertFalse(program.eval(token1, GrinTokenKind.LESS_THAN_OR_EQUAL, token2,None))
        self.assertTrue(program.eval(token1, GrinTokenKind.NOT_EQUAL, token2,None))
        self.assertFalse(program.eval(token1, GrinTokenKind.EQUAL, token2,None))
        self.assertRaises(GrinRuntimeException, program.eval, token1,GrinTokenKind.NOT_EQUAL, token3,None)

    def test_goto_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        program.add_raw('GOTO 2')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOTO,token1, None)
        self.assertEqual(program.counter, 4)
        program.jump(GrinTokenKind.GOTO, token2, None)
        self.assertEqual(program.counter, 3)




    def test_gosub_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        program.add_raw('GOSUB 2')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOSUB,token1, None)
        self.assertEqual(program.counter, 4)
        program.jump(GrinTokenKind.GOSUB, token2, None)
        self.assertEqual(program.counter, 3)

    def test_return_function(self):
        program = Program()
        program.add_raw('LET A 1')
        program.add_raw('LET B 2')
        program.add_raw('GOTO 2')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        program.add_raw('PRINT A')
        program.add_raw('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOSUB,token1, None)
        program.backtrack()
        self.assertEqual(program.counter,3)
        program.jump(GrinTokenKind.GOSUB, token2, None)
        program.backtrack()
        self.assertEqual(program.counter, 4)

if __name__ == '__main__':
    unittest.main()