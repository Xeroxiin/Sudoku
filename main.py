import game, solver, time

gs = game.Sudoku()
print(gs.showState())

s = solver.Solver(gs)

startTime = time.time()

lastFilledCellCount = gs.filledCells()

while not gs.solved:
    cfc = s.iterate()
    if cfc == lastFilledCellCount: break
    else: lastFilledCellCount = cfc
elapsedTime = time.time() - startTime
print(gs.showState())
if gs.sanityCheck() == True:
    print(f'Sudoku solved in {elapsedTime}s and passed final check.')
else:
    print(f'Sudoku completed in {elapsedTime}s but failed final check.')


