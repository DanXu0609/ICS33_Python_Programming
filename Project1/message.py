class Message:

    def __init__(self, msg, types, start, end, way):
        # types-> 0 cancel, 1 alert
        # way-> 0 received, 1 sent
        self.msg = msg
        self.types = types
        self.start = start
        self.end = end
        self.way = way

    def __repr__(self):
        direction = 'FROM' if self.way == 0 else 'TO'
        msg_type = 'CANCELLATION' if self.types == 0 else 'ALERT'
        action = 'RECEIVED' if self.way == 0 else 'SENT'
        if action == 'SENT':
            return f' #{self.start} {action} {msg_type} {direction} #{self.end}: {self.msg}'

        return f' #{self.end} {action} {msg_type} {direction} #{self.start}: {self.msg}'


    def __lt__(self, other):
        if self.way != other.way:
            return self.way < other.way
        elif self.types != other.types:
            return self.types < other.types
        elif self.msg != other.msg:
            return self.msg < other.msg
        else:
            return self.start < other.start if self.way == 0 else self.end < other.end