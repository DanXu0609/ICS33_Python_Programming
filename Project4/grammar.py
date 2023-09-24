from rule import Rule
class Grammar:
    def __init__(self):
        self.rules = {}

    def get_statements(self,file_name):
        with open(file_name,"r") as f:
            contents = f.readlines()

        self._make_rules(contents)

    def _make_rules(self, contents):
        ind = 0
        while ind < len(contents):
            s = contents[ind].strip()
            if s == '{':
                line = []
                next_line = contents[ind+1].strip()
                while next_line != '}' and ind < len(contents):
                    if next_line:
                        line.append(next_line)
                    ind += 1
                    next_line = contents[ind+1].strip()
                self._make_rule(line)

            ind += 1

    def _make_rule(self, rule_content):
        self.rules[rule_content[0]] = Rule(rule_content[0], rule_content[1:])

    def make_statements(self, start, count):
        res = []
        rule = self.rules[start]
        rule.start_dfs(res, int(count),self.rules)

        for statement in res:
            print(statement)