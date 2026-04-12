"""
Comprehensive tests for ttt.py — Cell, Board, and MoveAI classes.

Because ttt.py calls main() at module level (which blocks on input()),
we patch builtins.input with an EOFError side-effect so the import
completes immediately without hanging.
"""

import unittest
from unittest.mock import patch
import io
import sys

# ── import ttt without blocking on the interactive main() ──────────────────
# ttt.py calls main() at module level.  main() loops until "play again?" → 'n'.
# We supply enough position strings to survive one full game (max 4 player turns
# × up to 9 retries = 36 attempts), then 'n' to exit, then silence all printing.
_positions = [str(i % 9 + 1) for i in range(50)]  # cycles "1"–"9" repeatedly
_play_again = ['n']
with patch('builtins.input', side_effect=_positions + _play_again):
    with patch('builtins.print'):
        import ttt

from ttt import (
    Cell, Board, MoveAI,
    computerToken, playerToken, emptyToken,
)

# ═══════════════════════════════════════════════════════════════════════════
# Cell tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCell(unittest.TestCase):

    def test_init_stores_cellnum(self):
        cell = Cell(3)
        self.assertEqual(cell.getIndex(), 3)

    def test_init_token_is_empty(self):
        cell = Cell(0)
        self.assertEqual(cell.getToken(), emptyToken)

    def test_isEmpty_on_new_cell(self):
        cell = Cell(0)
        self.assertTrue(cell.isEmpty())

    def test_setToken_and_getToken(self):
        cell = Cell(1)
        cell.setToken(computerToken)
        self.assertEqual(cell.getToken(), computerToken)
        self.assertFalse(cell.isEmpty())

    def test_setToken_player(self):
        cell = Cell(2)
        cell.setToken(playerToken)
        self.assertEqual(cell.getToken(), playerToken)
        self.assertFalse(cell.isEmpty())

    def test_getIndex_all_positions(self):
        for i in range(9):
            self.assertEqual(Cell(i).getIndex(), i)


# ═══════════════════════════════════════════════════════════════════════════
# Board tests
# ═══════════════════════════════════════════════════════════════════════════

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    # ── initialisation ──────────────────────────────────────────────────
    def test_init_nine_cells(self):
        self.assertEqual(len(self.board.cells), 9)

    def test_init_all_cells_empty(self):
        for i in range(9):
            self.assertTrue(self.board.getCell(i).isEmpty())

    def test_init_eight_winning_moves(self):
        self.assertEqual(len(self.board.winningMoves), 8)

    def test_init_win_state_cleared(self):
        self.assertEqual(self.board.winToken, emptyToken)
        self.assertEqual(self.board.winMove, [])

    # ── reset ───────────────────────────────────────────────────────────
    def test_reset_clears_tokens(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(4, playerToken)
        self.board.reset()
        for i in range(9):
            self.assertTrue(self.board.getCell(i).isEmpty())

    def test_reset_clears_win_state(self):
        self.board.winToken = computerToken
        self.board.winMove  = [0, 1, 2]
        self.board.reset()
        self.assertEqual(self.board.winToken, emptyToken)
        self.assertEqual(self.board.winMove, [])

    # ── get/set cell token ──────────────────────────────────────────────
    def test_setCellToken_and_getCellToken(self):
        self.board.setCellToken(5, playerToken)
        self.assertEqual(self.board.getCellToken(5), playerToken)

    def test_getCell_returns_cell_object(self):
        cell = self.board.getCell(7)
        self.assertIsInstance(cell, Cell)
        self.assertEqual(cell.getIndex(), 7)

    # ── getBoardAsList ──────────────────────────────────────────────────
    def test_getBoardAsList_length(self):
        self.assertEqual(len(self.board.getBoardAsList()), 9)

    def test_getBoardAsList_reflects_tokens(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(8, playerToken)
        lst = self.board.getBoardAsList()
        self.assertEqual(lst[0], computerToken)
        self.assertEqual(lst[8], playerToken)
        self.assertEqual(lst[4], emptyToken)

    # ── getEmptyCells / movesExist ──────────────────────────────────────
    def test_getEmptyCells_full_board_is_empty(self):
        self.assertEqual(len(self.board.getEmptyCells()), 9)

    def test_getEmptyCells_after_moves(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(4, playerToken)
        empty = self.board.getEmptyCells()
        self.assertEqual(len(empty), 7)
        self.assertNotIn(0, empty)
        self.assertNotIn(4, empty)

    def test_movesExist_on_new_board(self):
        self.assertTrue(self.board.movesExist())

    def test_movesExist_false_when_full(self):
        tokens = [computerToken, playerToken] * 4 + [computerToken]
        for i in range(9):
            self.board.setCellToken(i, tokens[i])
        self.assertFalse(self.board.movesExist())

    # ── checkForWinner ──────────────────────────────────────────────────
    def _fill(self, cells, token):
        for c in cells:
            self.board.setCellToken(c, token)

    def test_checkForWinner_top_row(self):
        self._fill([0, 1, 2], computerToken)
        self.assertTrue(self.board.checkForWinner(computerToken))
        self.assertEqual(self.board.winToken, computerToken)
        self.assertEqual(self.board.winMove, [0, 1, 2])

    def test_checkForWinner_middle_row(self):
        self._fill([3, 4, 5], playerToken)
        self.assertTrue(self.board.checkForWinner(playerToken))

    def test_checkForWinner_bottom_row(self):
        self._fill([6, 7, 8], computerToken)
        self.assertTrue(self.board.checkForWinner(computerToken))

    def test_checkForWinner_left_col(self):
        self._fill([0, 3, 6], playerToken)
        self.assertTrue(self.board.checkForWinner(playerToken))

    def test_checkForWinner_middle_col(self):
        self._fill([1, 4, 7], computerToken)
        self.assertTrue(self.board.checkForWinner(computerToken))

    def test_checkForWinner_right_col(self):
        self._fill([2, 5, 8], playerToken)
        self.assertTrue(self.board.checkForWinner(playerToken))

    def test_checkForWinner_diagonal_tl_br(self):
        self._fill([0, 4, 8], computerToken)
        self.assertTrue(self.board.checkForWinner(computerToken))

    def test_checkForWinner_diagonal_tr_bl(self):
        self._fill([2, 4, 6], playerToken)
        self.assertTrue(self.board.checkForWinner(playerToken))

    def test_checkForWinner_no_winner(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(1, playerToken)
        self.assertFalse(self.board.checkForWinner(computerToken))
        self.assertFalse(self.board.checkForWinner(playerToken))

    def test_checkForWinner_wrong_token_no_match(self):
        self._fill([0, 1, 2], computerToken)
        self.assertFalse(self.board.checkForWinner(playerToken))

    # ── couldWin ────────────────────────────────────────────────────────
    def test_couldWin_detects_winning_move(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(1, computerToken)
        # cell 2 would complete top row
        self.assertTrue(self.board.couldWin(2, computerToken))

    def test_couldWin_does_not_modify_board(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(1, computerToken)
        self.board.couldWin(2, computerToken)
        self.assertTrue(self.board.getCell(2).isEmpty())

    def test_couldWin_returns_false_when_no_win(self):
        self.board.setCellToken(0, computerToken)
        self.assertFalse(self.board.couldWin(4, computerToken))

    def test_couldWin_player_block_scenario(self):
        self.board.setCellToken(6, playerToken)
        self.board.setCellToken(7, playerToken)
        # cell 8 would complete bottom row for player
        self.assertTrue(self.board.couldWin(8, playerToken))


# ═══════════════════════════════════════════════════════════════════════════
# MoveAI tests
# ═══════════════════════════════════════════════════════════════════════════

class TestMoveAI(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.ai    = MoveAI(self.board)

    # ── rotatePattern ───────────────────────────────────────────────────
    def test_four_rotations_return_to_original(self):
        pat = ['0','1','2','3','4','5','6','7','8']
        result = pat
        for _ in range(4):
            result = self.ai.rotatePattern(result)
        self.assertEqual(result, pat)

    def test_rotate_known_pattern(self):
        # top row [0,1,2] should become right column [2,5,8] after one CW rotation
        pat = ['X','X','X','b','b','b','b','b','b']
        rot = self.ai.rotatePattern(pat)
        # after CW rotation: indices map [6,3,0,7,4,1,8,5,2]
        # original: 6=b,3=b,0=X,7=b,4=b,1=X,8=b,5=b,2=X
        expected = ['b','b','X','b','b','X','b','b','X']
        self.assertEqual(rot, expected)

    # ── mirrorPattern ───────────────────────────────────────────────────
    def test_two_mirrors_return_to_original(self):
        pat = ['0','1','2','3','4','5','6','7','8']
        result = self.ai.mirrorPattern(self.ai.mirrorPattern(pat))
        self.assertEqual(result, pat)

    def test_mirror_known_pattern(self):
        pat = ['X','b','b','b','b','b','b','b','b']
        m   = self.ai.mirrorPattern(pat)
        # mirror indices [2,1,0,5,4,3,8,7,6]: position 0 gets original[2]=b, position 2 gets original[0]=X
        self.assertEqual(m[2], 'X')
        self.assertEqual(m[0], 'b')

    # ── isUniquePattern ─────────────────────────────────────────────────
    def test_isUniquePattern_true_for_new(self):
        ai = MoveAI.__new__(MoveAI)
        ai.patterns = []
        self.assertTrue(ai.isUniquePattern(['a','b']))

    def test_isUniquePattern_false_for_duplicate(self):
        ai = MoveAI.__new__(MoveAI)
        ai.patterns = [['X','O','b']]
        self.assertFalse(ai.isUniquePattern(['X','O','b']))

    # ── makeAllPatterns / pattern count ────────────────────────────────
    def test_patterns_expanded_from_base(self):
        self.assertGreater(len(self.ai.patterns), len(self.ai.basePatterns))

    def test_all_patterns_have_nine_elements(self):
        for p in self.ai.patterns:
            self.assertEqual(len(p), 9, f"Pattern has wrong length: {p}")

    def test_all_patterns_have_a_move_marker(self):
        for p in self.ai.patterns:
            self.assertIn('*', p, f"Pattern has no '*': {p}")

    def test_no_duplicate_patterns(self):
        seen = []
        for p in self.ai.patterns:
            self.assertNotIn(p, seen, f"Duplicate pattern: {p}")
            seen.append(p)

    # ── cellMatch ───────────────────────────────────────────────────────
    def test_cellMatch_b_matches_empty(self):
        self.assertTrue(self.ai.cellMatch(emptyToken, 'b'))

    def test_cellMatch_star_matches_empty(self):
        self.assertTrue(self.ai.cellMatch(emptyToken, '*'))

    def test_cellMatch_O_matches_player(self):
        self.assertTrue(self.ai.cellMatch(playerToken, 'O'))

    def test_cellMatch_X_matches_computer(self):
        self.assertTrue(self.ai.cellMatch(computerToken, 'X'))

    def test_cellMatch_question_matches_anything(self):
        self.assertTrue(self.ai.cellMatch(emptyToken,    '?'))
        self.assertTrue(self.ai.cellMatch(computerToken, '?'))
        self.assertTrue(self.ai.cellMatch(playerToken,   '?'))

    def test_cellMatch_b_does_not_match_token(self):
        self.assertFalse(self.ai.cellMatch(computerToken, 'b'))
        self.assertFalse(self.ai.cellMatch(playerToken,   'b'))

    def test_cellMatch_O_does_not_match_computer(self):
        self.assertFalse(self.ai.cellMatch(computerToken, 'O'))

    def test_cellMatch_X_does_not_match_player(self):
        self.assertFalse(self.ai.cellMatch(playerToken, 'X'))

    # ── findMoveInPattern ───────────────────────────────────────────────
    def test_findMoveInPattern_finds_star(self):
        pattern = ['b','b','b','b','*','b','b','b','b']
        self.assertEqual(self.ai.findMoveInPattern(pattern), 4)

    def test_findMoveInPattern_raises_if_no_star(self):
        pattern = ['b','b','b','b','b','b','b','b','b']
        with self.assertRaises(Exception):
            self.ai.findMoveInPattern(pattern)

    # ── mustWinMove ─────────────────────────────────────────────────────
    def test_mustWinMove_finds_winning_cell(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(1, computerToken)
        cell = self.ai.mustWinMove()
        self.assertEqual(cell, 2)

    def test_mustWinMove_returns_minus1_when_none(self):
        cell = self.ai.mustWinMove()
        self.assertEqual(cell, -1)

    def test_mustWinMove_column_win(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(3, computerToken)
        cell = self.ai.mustWinMove()
        self.assertEqual(cell, 6)

    def test_mustWinMove_diagonal_win(self):
        self.board.setCellToken(0, computerToken)
        self.board.setCellToken(4, computerToken)
        cell = self.ai.mustWinMove()
        self.assertEqual(cell, 8)

    # ── mustBlockMove ───────────────────────────────────────────────────
    def test_mustBlockMove_finds_blocking_cell(self):
        self.board.setCellToken(6, playerToken)
        self.board.setCellToken(7, playerToken)
        cell = self.ai.mustBlockMove()
        self.assertEqual(cell, 8)

    def test_mustBlockMove_returns_minus1_when_none(self):
        cell = self.ai.mustBlockMove()
        self.assertEqual(cell, -1)

    def test_mustBlockMove_column_block(self):
        self.board.setCellToken(2, playerToken)
        self.board.setCellToken(5, playerToken)
        cell = self.ai.mustBlockMove()
        self.assertEqual(cell, 8)

    # ── computerMove priority: win > block > pattern > random ───────────
    def test_computerMove_takes_win_over_block(self):
        """Computer should win rather than just block."""
        # Computer has [3,4], player has [0,1] — both need index 5 / 2.
        # Computer needs cell 5 to win (row 3-4-5), player needs cell 2.
        self.board.setCellToken(3, computerToken)
        self.board.setCellToken(4, computerToken)
        self.board.setCellToken(0, playerToken)
        self.board.setCellToken(1, playerToken)
        self.ai.computerMove()
        self.assertEqual(self.board.getCellToken(5), computerToken)

    def test_computerMove_blocks_player_win(self):
        """Computer must block when player is about to win."""
        self.board.setCellToken(6, playerToken)
        self.board.setCellToken(7, playerToken)
        self.ai.computerMove()
        self.assertEqual(self.board.getCellToken(8), computerToken)

    def test_computerMove_places_token_on_empty_cell(self):
        """Any computer move lands on an empty cell."""
        # Give it a non-trivial board state without immediate win/block
        self.board.setCellToken(4, computerToken)
        self.board.setCellToken(0, playerToken)
        empty_before = set(self.board.getEmptyCells())
        self.ai.computerMove()
        empty_after  = set(self.board.getEmptyCells())
        moved_to = empty_before - empty_after
        self.assertEqual(len(moved_to), 1)
        cell = list(moved_to)[0]
        self.assertEqual(self.board.getCellToken(cell), computerToken)

    def test_computerMove_doesnt_overwrite_existing_token(self):
        """Computer move must not land on an occupied cell."""
        for i in range(8):
            token = computerToken if i % 2 == 0 else playerToken
            self.board.setCellToken(i, token)
        # Only cell 8 is free
        self.ai.computerMove()
        # Board now has exactly the tokens we set plus cell 8 = computer
        self.assertEqual(self.board.getCellToken(8), computerToken)

    # ── Full game simulation: computer never loses ──────────────────────
    def _simulate_random_game(self, seed):
        """Play a full game with random player moves. Returns 'computer', 'player', or 'tie'."""
        import random
        rng = random.Random(seed)

        board = Board()
        ai    = MoveAI(board)
        ai.computerMove()  # computer always goes first

        while True:
            if board.checkForWinner(computerToken):
                return 'computer'
            empty = board.getEmptyCells()
            if not empty:
                return 'tie'

            # Random player move
            cell = rng.choice(empty)
            board.setCellToken(cell, playerToken)

            if board.checkForWinner(playerToken):
                return 'player'
            if not board.movesExist():
                return 'tie'

            ai.computerMove()

    def test_computer_never_loses_100_games(self):
        """Play 100 games with random player moves — computer must never lose."""
        losses = []
        for seed in range(100):
            result = self._simulate_random_game(seed)
            if result == 'player':
                losses.append(seed)
        self.assertEqual(losses, [],
            f"Computer lost {len(losses)} game(s) with seeds: {losses}")

    def test_game_ends_when_board_full(self):
        """A full board with no winner is a tie — movesExist returns False."""
        # Forced tie board: X O X / X X O / O X O  — no winner
        tokens = [computerToken, playerToken, computerToken,
                  computerToken, computerToken, playerToken,
                  playerToken,   computerToken, playerToken]
        for i, t in enumerate(tokens):
            self.board.setCellToken(i, t)
        self.assertFalse(self.board.checkForWinner(computerToken))
        self.assertFalse(self.board.checkForWinner(playerToken))
        self.assertFalse(self.board.movesExist())


# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    unittest.main(verbosity=2)
