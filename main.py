import game, solver, time

gs = game.Sudoku()
print(gs.showState())

s = solver.Solver(gs)

startTime = time.time()
while not gs.solved:
    s.iterate()
elapsedTime = time.time() - startTime
print(gs.showState())
if gs.sanityCheck() == True:
    print(f'Sudoku solved in {elapsedTime}s and passed sanity check.')
else:
    print(f'Sudoku completed in {elapsedTime}s but failed sanity check.')


