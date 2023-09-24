
from option import Option
import random
class Rule:
    def __init__(self, name, options):
        self.name = name
        self.options = self.make_option(options)
        self.sum = self._make_sum()
        self.intervals = self.make_prob()
    def make_option(self, options):
        res = []
        for option in options:
            res.append(Option(option))

        return res

    def _make_sum(self):
        return sum([opt.weight for opt in self.options])

    def pick_option(self):
        val = random.randint(0,self.sum-1)
        index = self._binary_search(val)
        return self.options[index]
    def _binary_search(self,val):
        l = 0
        r = len(self.intervals)
        while l < r:
            m = (l + r) // 2
            if self.intervals[m] > val:
                r = m
            elif self.intervals[m] < val:
                l = m + 1
            else:
                return m + 1
        return l
    def make_prob(self):
        intervals = []
        for ind in range(len(self.options)):
            if intervals:
                intervals.append(self.options[ind].weight + intervals[ind-1])
            else:
                intervals.append(self.options[ind].weight)

        return intervals

    def start_dfs(self, res, count, rules):
        while count > 0:
            cur = []
            opt = self.pick_option()
            rule = opt.dfs(cur, rules)
            res.append(rule)
            count -= 1