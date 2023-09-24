import unittest
from command import Command
from helper import recursion, display_result, read_files
from message import Message
class TestSimulation(unittest.TestCase):
    def test_message_diff_by_action(self):
        m1 = Message(msg = 'hello', types = 0, start = 1, end = 2, way = 0)
        m2 = Message(msg = 'hello', types = 0, start = 1, end = 2, way = 1)

        self.assertLess(m1,m2)

    def test_message_diff_by_types(self):
        m3 = Message(msg = 'hello', types = 0, start = 1, end = 2, way = 0)
        m4 = Message(msg = 'hello', types = 1, start = 1, end = 2, way = 0)

        self.assertLess(m3, m4)

    def test_message_diff_by_start(self):
        m5 = Message(msg = 'hello', types = 0, start = 0, end = 2, way = 0)
        m6 = Message(msg = 'hello', types = 0, start = 1, end = 2, way = 0)

        self.assertLess(m5,m6)

    def test_message_diff_by_end(self):
        m7 = Message(msg = 'hello', types = 0, start = 1, end = 0, way = 1)
        m8 = Message(msg = 'hello', types = 0, start = 1, end = 2, way = 1)

        self.assertLess(m7,m8)

    def test_message_diff_by_msg(self):
        m9 = Message(msg = 'BOO', types = 0, start = 1, end = 0, way = 1)
        m10 = Message(msg = 'BO', types = 0, start = 1, end = 0, way = 1)

        self.assertLess(m10,m9)

    def test_message_repr(self):
        m9 = Message(msg = 'BOO', types = 0, start = 1, end = 0, way = 1)
        m5 = Message(msg = 'hello', types = 0, start = 0, end = 2, way = 0)

        self.assertEqual(' #2 RECEIVED CANCELLATION FROM #0: hello', repr(m5))

        self.assertEqual(' #1 SENT CANCELLATION TO #0: BOO', repr(m9))

    def test_command_diff(self):
        c1 = Command(msg = 'BOO', types = 0, node = 1, time = 0)
        c2 = Command(msg = 'hello', types = 0, node =1, time = 0)
        Command.add(c1)
        Command.add(c2)
        self.assertLess(c1,c2)

    def test_command_type_diff(self):
        c3 = Command(msg = 'BOO', types = 0, node = 1, time = 0)
        c4 = Command(msg = 'BOO', types = 1, node = 1, time = 0)
        Command.add(c3)
        Command.add(c4)
        self.assertLess(c3,c4)

    def test_command_time_diff(self):
        c5 = Command(msg = 'BOO', types = 0, node = 1, time = 0)
        c6 = Command(msg = 'BOO', types = 0, node = 1, time = 100)
        Command.add(c5)
        Command.add(c6)
        self.assertLess(c5,c6)
    def test_command_node_diff(self):
        c7 = Command(msg = 'BOO', types = 0, node = 0, time = 0)
        c8 = Command(msg = 'BOO', types = 0, node = 1, time = 0)
        Command.add(c7)
        Command.add(c8)
        self.assertLess(c7,c8)

    def test_commands_size(self):
        self.assertEqual(8, len(Command.commands))
        Command.pop()
        Command.clear()
        self.assertEqual(0, len(Command.commands))

    def test_output_file(self):
        import os
        import io
        from unittest.mock import patch
        path = os.path.join(os.pardir, 'samples', 'sample_input.txt')
        graph = {}
        result = {}
        received_cancel = {}
        with open(path, 'r') as f:
            length = read_files(f,graph)


        for command in Command.commands:
            time = command.time
            start = command.node
            types = command.types
            msg = command.msg
            recursion(graph, result, -1, start, time, types, msg, set(), received_cancel, length)

        with patch('sys.stdout', new=io.StringIO()) as output:
            display_result(result, length)

        expected_output = """
@0: #1 SENT ALERT TO #2: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@750: #2 SENT ALERT TO #3: Trouble
@2000: #3 RECEIVED ALERT FROM #2: Trouble
@2000: #3 SENT ALERT TO #4: Trouble
@2200: #1 SENT CANCELLATION TO #2: Trouble
@2500: #4 RECEIVED ALERT FROM #3: Trouble
@2500: #4 SENT ALERT TO #1: Trouble
@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble
@2950: #2 SENT CANCELLATION TO #3: Trouble
@3500: #1 RECEIVED ALERT FROM #4: Trouble
@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble
@4200: #3 SENT CANCELLATION TO #4: Trouble
@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble
@4700: #4 SENT CANCELLATION TO #1: Trouble
@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble
@120000: END
"""
        self.assertEqual(expected_output.strip(),output.getvalue().strip())






