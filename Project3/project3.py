# project3.py
#
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin
from context import Program

def main() -> None:
    program = Program()

    while True:
        statement = input()
        if statement.strip() == '.':
            break
        program.add_raw(statement)


    program.preprocess()
    # print(program.functions)
    while program.runnable():
        line = program.get_statement()
        keyword_kind = line[0].kind()
        if keyword_kind in program.std:
            program.io(keyword_kind, line[1])
            program.forward()
        elif keyword_kind in program.operation:
            program.op(keyword_kind, line[1],line[2])
            program.forward()
        elif keyword_kind == grin.GrinTokenKind.END:
            program.end()
        elif keyword_kind in program.branch:
            program.jump(keyword_kind, line[1], line[0].location())\
            if len(line) < 3 or program.eval(line[3],line[4].kind(),line[5],line[4].location())\
            else program.forward()
        elif keyword_kind == program.back:
            program.backtrack()





    # for line in program.program:
    #     for token in line:
    #         print(token.value(), token.kind())




if __name__ == '__main__':
    main()
