# sudoku_clean.py

class Sudoku:
    """
    Minimal Sudoku solver:
      - Constraint-propagation step: solve()
      - Full solver with guessing/backtracking: solve_backtrack()
    Board format: 9x9 list of lists with 0 for empty cells.
    """

    def __init__(self, A):
        self.S = A          # board
        self.N = {}         # neighbors map: (r,c) -> set[(nr,nc)]
        self.find_neighbors()
        self.init_valid()   # V: valid values per cell

    def find_neighbors(self):
        """Precompute neighbor cells for each position (same row, col, box)."""
        for r in range(9):
            for c in range(9):
                neighbors = set()

                # row & column
                for col in range(9):
                    if col != c:
                        neighbors.add((r, col))
                for row in range(9):
                    if row != r:
                        neighbors.add((row, c))

                # 3x3 box
                firstrow = 3 * (r // 3)
                firstcol = 3 * (c // 3)
                for i in range(firstrow, firstrow + 3):
                    for j in range(firstcol, firstcol + 3):
                        if (i, j) != (r, c):
                            neighbors.add((i, j))

                self.N[(r, c)] = neighbors

    def init_valid(self):
        """Initialize V[(r,c)] = set of valid digits for each empty cell."""
        self.V = {}
        for r in range(9):
            for c in range(9):
                if self.S[r][c] != 0:
                    self.V[(r, c)] = set()
                else:
                    possible = set(range(1, 10))
                    for (nr, nc) in self.N[(r, c)]:
                        if self.S[nr][nc] != 0:
                            possible.discard(self.S[nr][nc])
                    self.V[(r, c)] = possible

    def solve(self):
        """
        Repeatedly fill any cell that has a single valid value.
        Returns: 1 if solved, 0 if stuck (needs guessing), -1 if contradiction.
        """
        known = {(val, r, c) for (r, c), vals in self.V.items() if len(vals) == 1 for val in vals}

        # No forced moves:
        if not known:
            if all(self.S[r][c] != 0 for r in range(9) for c in range(9)):
                return 1     # filled = solved
            return 0         # needs backtracking

        # Apply forced moves
        for val, r, c in known:
            self.S[r][c] = val
            self.V[(r, c)] = set()

            # Remove val from neighbors' valid sets; detect contradictions
            for nr, nc in self.N[(r, c)]:
                if val in self.V[(nr, nc)]:
                    self.V[(nr, nc)].discard(val)
                    if len(self.V[(nr, nc)]) == 0 and self.S[nr][nc] == 0:
                        return -1  # contradiction

        # Keep propagating
        return self.solve()

    def solve_backtrack(self):
        """
        Full solver with guessing/backtracking.
        Chooses the most constrained empty cell (smallest |V|) first.
        Returns: 1 if solved, 0 if needs alternative guesses, -1 if unsolvable.
        """
        # Pick an empty cell with the fewest candidates (MRV heuristic)
        empty_cells = [(len(self.V[(r, c)]), r, c)
                       for r in range(9) for c in range(9) if self.S[r][c] == 0]
        if not empty_cells:
            return 1  # solved

        empty_cells.sort()
        r, c = empty_cells[0][1], empty_cells[0][2]

        for val in list(self.V[(r, c)]):
            # Place a guess
            self.S[r][c] = val

            # Temporarily update neighbors' valid sets; track changes
            affected_neighbors = {}
            valid_move = True
            for nr, nc in self.N[(r, c)]:
                if val in self.V[(nr, nc)]:
                    affected_neighbors[(nr, nc)] = self.V[(nr, nc)].copy()
                    self.V[(nr, nc)].discard(val)

                    # If a neighbor is empty and now has no candidates, dead end
                    if len(self.V[(nr, nc)]) == 0 and self.S[nr][nc] == 0:
                        valid_move = False
                        break

            # Recurse if still consistent
            if valid_move:
                result = self.solve_backtrack()
                if result == 1:
                    return 1

            # Undo guess and candidate prunes (backtrack)
            self.S[r][c] = 0
            for (nr, nc), original_values in affected_neighbors.items():
                self.V[(nr, nc)] = original_values

        # If none of the candidates worked:
        if not any(len(self.V[(r, c)]) > 0 for _, r, c in empty_cells):
            return -1  # no candidates anywhere → unsolvable in this branch

        return 0
if __name__ == "__main__":
    # Example Sudoku board (0 = empty)
    board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]

    s = Sudoku(board)
    result = s.solve()

    # If logic step got stuck, fall back to backtracking
    if result != 1:
        s.solve_backtrack()

    for r in range(9):
        print(s.S[r])
