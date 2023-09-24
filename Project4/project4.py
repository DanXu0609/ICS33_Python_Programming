# project4.py
#
# ICS 33 Winter 2023
# Project 4: Still Looking for Something

from grammar import Grammar
def main() -> None:
    path = input()
    count = input()
    start = input()
    g = Grammar()
    g.get_statements(path)
    g.make_statements(start,count)


if __name__ == '__main__':
    main()
