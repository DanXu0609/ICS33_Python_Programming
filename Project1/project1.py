from pathlib import Path

from command import Command
from helper import recursion, display_result, read_files
import os

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    graph ={}
    result = {}
    received_cancel = {}

    with open(input_file_path, 'r') as f:
        length = read_files(f,graph)

    for command in Command.commands:
        time = command.time
        start = command.node
        types = command.types
        msg = command.msg
        recursion(graph,result, -1, start, time, types, msg, set(),received_cancel,length)

    display_result(result,length)

if __name__ == '__main__':
    main()
