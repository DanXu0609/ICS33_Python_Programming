# test_queens.py
#
# ICS 33 Winter 2023
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_zero_queen_count_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState, Position
import unittest



class TestQueensState(unittest.TestCase):
    def test_zero_queen_count_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_invalid_size_board_error(self):
        from queens import InvalidValueError
        self.assertRaises(InvalidValueError, QueensState.__init__,self,rows = 5, columns = 0)
        self.assertRaises(InvalidValueError, QueensState.__init__, self, rows = -1, columns = -1)

        with self.assertRaises(InvalidValueError) as context:
            raise InvalidValueError(-1,-1)
        self.assertTrue('We have invalid value in row -1 or column -1' in str(context.exception))




    def test_duplicat_queen_error(self):
        from queens import DuplicateQueenError
        state = QueensState(9,9)
        state = state.with_queens_added(positions = [Position(0,0)])
        self.assertRaises(DuplicateQueenError, state.with_queens_added, positions=[Position(0,0)])

        with self.assertRaises(DuplicateQueenError) as context:
            raise DuplicateQueenError(Position(3,4))
        self.assertTrue('duplicate queen in row 3 column 4' in str(context.exception))

    def test_out_of_board_error(self):
        from queens import OutOfBoardError
        state = QueensState(6,9)
        self.assertRaises(OutOfBoardError, state.with_queens_added,
                          positions = [Position(10, 8)])
        self.assertRaises(OutOfBoardError, state.with_queens_removed,
                          positions = [Position(10, 8)])

        with self.assertRaises(OutOfBoardError) as context:
            raise OutOfBoardError(Position(3,4))
        self.assertTrue('queen is placed out of board in row 3 column 4' in str(context.exception))

    def test_missing_queen_error(self):
        from queens import MissingQueenError
        state = QueensState(7,16)
        self.assertRaises(MissingQueenError, state.with_queens_removed, positions = [Position(5,12)])

        with self.assertRaises(MissingQueenError) as context:
            raise MissingQueenError(Position(3,4))
        self.assertTrue('missing queen in row 3 column 4' in str(context.exception))
    def test_queen_count(self):
        state = QueensState(12, 12)
        state.with_queens_added(positions = [Position(3, 1), Position(6, 6)])
        self.assertEqual(state.queen_count(), 2)
        state.with_queens_removed(positions = [Position(3, 1)])
        self.assertEqual(state.queen_count(), 1)


    def test_queens_list(self):
        q = [Position(1, 1), Position(2, 2)]
        state = QueensState(3, 3)

        state.with_queens_added(q)
        self.assertEqual(state.queens(), q)


    def test_has_queen(self):
        state = QueensState(15, 18)
        state.with_queens_added(positions = [Position(11, 11),Position(13,15)])
        self.assertTrue(state.has_queen(position = Position(11, 11)))
        self.assertFalse(state.has_queen(position = Position(1, 2)))
        self.assertTrue(state.has_queen(position = Position(13,15)))
        state.with_queens_removed(positions = [Position(13,15)])
        self.assertFalse(state.has_queen(position = Position(13,15)))

    def test_queens_unsafe(self):
        unsafe_row_state = QueensState(6,6)
        unsafe_row_state.with_queens_added(positions = [Position(2,1),Position(2,3)])
        self.assertTrue(unsafe_row_state.any_queens_unsafe())

        unsafe_column_state = QueensState(6,6)
        unsafe_column_state.with_queens_added(positions = [Position(5,1),Position(2,1)])
        self.assertTrue(unsafe_column_state.any_queens_unsafe())

        unsafe_diag_state = QueensState(6,6)
        unsafe_diag_state.with_queens_added(positions = [Position(0,0),Position(1,1),Position(2,2)])
        self.assertTrue(unsafe_diag_state.any_queens_unsafe())

        unsafe_anti_diag_state = QueensState(6,6)
        unsafe_anti_diag_state.with_queens_added(positions = [Position(2,2),Position(1,3)])
        self.assertTrue(unsafe_anti_diag_state.any_queens_unsafe())

    def test_queens_safe(self):
        state = QueensState(6,6)
        state.with_queens_added(positions = [Position(0,3),Position(1,1),Position(3,4)])
        self.assertFalse(state.any_queens_unsafe())




if __name__ == '__main__':
    unittest.main()
