
from symbol import Symbol

class Option:
    def __init__(self, content):
        self.weight = int(content[0])
        self.symbols = self.find_symbols(content.strip())

    def find_symbols(self, content):
        res = []

        list_of_words = content.split()[1:]
        for word in list_of_words:
            if '[' in word and ']' in word:
                sym = Symbol(word[1:][:-1],True)
            else:
                sym = Symbol(word,False)

            res.append(sym)

        return res

    def dfs(self, cur, rules):
        for symbol in self.symbols:
            if symbol.is_variable:
                sub_res = rules[symbol.content].pick_option().dfs([],rules)
                cur.append(sub_res)
            else:
                cur.append(symbol.content)

        return ' '.join(cur)

