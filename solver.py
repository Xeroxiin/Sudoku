from itertools import combinations

class Solver:
    def __init__(self, game):
        self.game = game
        self.known = game.grid
        self.notation = {}

    def setupNotation(self):
        for y in range(9):
            for x in range(9):
                if self.known[(x, y)].locked == True:
                    self.notation[(x, y)] = [None]
                else:
                    self.notation[(x, y)] = []

    def findMising(self, has):
        return [missing for missing in list(range(1, 10)) if not missing in has]

    def findHiddenSingles(self, cells):
        moves = []
        for digit in range(1, 10):
            possibleCells = [
                cell for cell in cells
                if self.notation[cell] != [None]
                and digit in self.notation[cell]
            ]

            if len(possibleCells) == 1:
                moves.append((possibleCells[0], digit))
        return moves

    def getEmptyCells(self, cells):
        return [cell for cell in cells if self.notation[cell] != [None]]

    def findNakedSets(self, cells):
        emptyCells = self.getEmptyCells(cells)
        nE = min(len(emptyCells)+1, 5)

        for n in range(2, nE):
            for combination in combinations(emptyCells, n):
                candidates = set()

                for cell in combination:
                    candidates.update(self.notation[cell])
                if len(candidates) == n:
                    for cell in cells:
                        if not cell in combination:
                            for candidate in candidates:
                                if candidate in self.notation[cell]:
                                    self.notation[cell].remove(candidate)

    def findHiddenSets(self, cells):
        emptyCells = self.getEmptyCells(cells)
        nE = min(len(emptyCells) + 1, 5)

        for n in range(2, nE):
            for combination in combinations(range(1, 10), n):
                possibleCells = set()
                valid = True

                for digit in combination:
                    digitCells = set()
                    for cell in emptyCells:
                        if digit in self.notation[cell]:
                            digitCells.add(cell)

                    if len(digitCells) == 0:
                        valid = False
                        break
                    possibleCells.update(digitCells)

                if valid and len(possibleCells) == n:
                    print("Hidden set:", combination, possibleCells)
                    for cell in possibleCells:
                        self.notation[cell] = [
                            candidate
                            for candidate in self.notation[cell]
                            if candidate in combination
                        ]
                    return
                     
    
    def findPointing(self, unit):
        for digit in range(1, 10):
            possibleCells = []
            for cell in unit:
                if digit in self.notation[cell]:
                    possibleCells.append(cell)

            if len(set([cell[0] for cell in possibleCells])) == 1:
                for otherCell in self.game.getColumn(possibleCells[0]):
                    if not otherCell in unit:
                        if digit in self.notation[otherCell]:
                            self.notation[otherCell].remove(digit)

            if len(set([cell[1] for cell in possibleCells])) == 1:
                for otherCell in self.game.getRow(possibleCells[0]):
                    if not otherCell in unit:
                        #not in target row
                        if digit in self.notation[otherCell]:
                            self.notation[otherCell].remove(digit)


    def getPossibleValues(self, cell):
        results = []
        rowValues = [self.game.getValue(v) for v in self.game.getRow(cell)]
        columnValues = [self.game.getValue(v) for v in self.game.getColumn(cell)]
        quadrantValues = [self.game.getValue(v) for v in self.game.getQuadrant(cell)]
        for digit in range(1,10):
            if digit not in rowValues and digit not in columnValues and digit not in quadrantValues:
                results.append(digit)
        return results
    
    def iterate(self):
        self.setupNotation()

        for x in range(9):
            for y in range(9):
                if self.notation[(x, y)] != [None]:
                    self.notation[(x, y)] = self.getPossibleValues((x, y))

        for y in range(9):
            self.findNakedSets(self.game.getRow((0, y)))

        for x in range(9):
            self.findNakedSets(self.game.getColumn((x, 0)))

        for anchor in self.game.quadrantAnchors:
            self.findNakedSets(self.game.getQuadrant(anchor))

        for anchor in self.game.quadrantAnchors:
            self.findPointing(self.game.getQuadrant(anchor))

        for y in range(9):
            self.findHiddenSets(self.game.getRow((0, y)))
        print("Notation after hidden sets:")
        for y in range(9):
            print([
                self.notation[(x, y)]
                for x in range(9)
            ])
        for x in range(9):
            self.findHiddenSets(self.game.getColumn((x, 0)))
        

        for anchor in self.game.quadrantAnchors:
            self.findHiddenSets(self.game.getQuadrant(anchor))
        
        moves = []

        moves += [
            (cell, v[0])
            for cell, v in self.notation.items()
            if self.notation[cell] != [None] and len(v) == 1
        ]

        for y in range(9):
            moves += self.findHiddenSingles(
                self.game.getRow((0, y))
            )

        for x in range(9):
            moves += self.findHiddenSingles(
                self.game.getColumn((x, 0))
            )

        for anchor in self.game.quadrantAnchors:
            moves += self.findHiddenSingles(
                self.game.getQuadrant(anchor)
            )

        for m in moves:
            self.game.addDigit(m[0], m[1])

        self.game.solved = not None in [
            self.game.getValue(v) for v in self.game.grid
        ]

        return self.game.filledCells()