# Sudoku Solver (Python)

A compact Sudoku solver built in Python that uses **constraint propagation** and **backtracking search** to fill any valid 9×9 Sudoku board.  
Includes both a logical deduction method and a recursive backtracking algorithm for more complex puzzles.

---

## Features
- Dual solving modes:
  - **Logic solver** – fills cells that have only one valid value.
  - **Backtracking solver** – recursive search for full completion.
- Automatically detects contradictions or unsolvable puzzles.
- Clean modular code in a single class (`Sudoku`) for easy reuse.

---

## How It Works
1. Builds a **neighbor map** for each cell (row, column, box).  
2. Tracks all **valid values** for every empty cell.  
3. Repeatedly applies logical deduction until stuck.  
4. Uses **backtracking** to test and revert guesses safely.  

---

## Run Locally
```bash
# Clone this repository
git clone https://github.com/mdacosta11/sudoku-solver.git
cd sudoku-solver

# Run the solver
python sudoku_clean.py
```
## Tech

Language: Python 3.10+

Core Concepts: recursion, constraint propagation, backtracking search

## Future Improvements

Add command-line input for custom boards

Visual GUI using Tkinter or Pygame

Benchmark solver performance on large puzzle sets

## Author

Michael Acosta
