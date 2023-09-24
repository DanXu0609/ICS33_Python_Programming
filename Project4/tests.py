import unittest
from symbol import Symbol
from grammar import Grammar
from option import Option
class TestProject4(unittest.TestCase):
    def test_symbol(self):
        se1 = Symbol('Boo',False)
        se2 = Symbol('Adj',True)
        self.assertEqual(se1.content,'Boo')
        self.assertTrue(se2.is_variable)

    def test_create_rules(self):
        g = Grammar()
        g.get_statements('input.txt')

        self.assertTrue('HowIsBoo' in g.rules)
        self.assertTrue('Adjective' in g.rules)

        self.assertEqual(len(g.rules['HowIsBoo'].options),1)
        self.assertEqual(len(g.rules['Adjective'].options), 5)

    def test_total_weights(self):
        g = Grammar()
        g.get_statements('input.txt')
        self.assertEqual(g.rules['HowIsBoo'].sum,1)
        self.assertEqual(g.rules['Adjective'].sum, 10)

if __name__ == '__main__':
    unittest.main()


