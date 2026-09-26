import game, solver

gs = game.Sudoku()
print(gs.showState())

s = solver.Solver(gs)
s.iterate()

