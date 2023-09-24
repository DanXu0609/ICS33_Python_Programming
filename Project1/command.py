import heapq
class Command:
    commands = []

    def __init__(self, msg, time, node, types):
        self.msg = msg
        self.time = time
        self.node = node
        self.types = types


    @staticmethod
    def add(command):
        heapq.heappush(Command.commands, command)
    @staticmethod
    def clear():
        Command.commands = []
    @staticmethod
    def pop():
        return heapq.heappop(Command.commands)

    def __lt__(self, other):
        if self.types != other.types:
            return self.types < other.types
        elif self.time != other.time:
            return self.time < other.time
        elif self.node != other.node:
            return self.node < other.node
        else:
            return self.msg < other.msg