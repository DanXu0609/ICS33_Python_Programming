# queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'





class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'

class OutOfBoardError(Exception):

    def __init__(self,position: Position):

        self._position = position

    def __str__(self) -> str:

        return f'queen is placed out of board in row {self._position.row} column {self._position.column}'

class InvalidValueError(Exception):

    def __init__(self,row,column):
        self.row = row
        self.column = column

    def __str__(self):
        return f'We have invalid value in row {self.row} or column {self.column}'
class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        if rows <= 0 or columns <= 0:
            raise InvalidValueError(rows,columns)
        self._rows = rows
        self._columns = columns
        self._board = set()


    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        return len(self._board)


    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        return list(self._board)



    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        return position in self._board


    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        rows = set()
        columns = set()
        diag = set()
        anti_diag = set()

        for position in self._board:
            i = position.row
            j = position.column
            if i in rows or j in columns or (i - j) in diag or (i + j) in anti_diag:
                return True

            rows.add(i)
            columns.add(j)
            diag.add(i - j)
            anti_diag.add(i + j)

        return False



    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions.
        Raises a DuplicateQueenException when there is already a queen in at
        least one of the given positions."""


        for position in positions:
            if position.row >= self._rows or position.row < 0 or position.column >= self._columns or position.column < 0:
                raise OutOfBoardError(position)
            elif position in self._board:
                raise DuplicateQueenError(position)



        self._board.update(positions)
        return self

    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions.
        Raises a MissingQueenException when there is no queen in at least one of
        the given positions."""
        for position in positions:
            if position.row >= self._rows or position.row < 0 or position.column >= self._columns or position.column < 0:
                raise OutOfBoardError(position)
            elif position not in self._board:
                raise MissingQueenError(position)


        self._board = self._board - set(positions)
        return self

