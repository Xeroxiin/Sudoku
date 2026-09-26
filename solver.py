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

    def findNakedPairs(self, cells):
        pairs = []
        for cell in cells:
            candi = self.notation[cell]
            if len(candi) == 2 and not candi in pairs:
                pairs.append(candi)

        for pair in pairs:
            cellsWithPair = []
            for cell in cells:
                if self.notation[cell] == pair:
                    cellsWithPair.append(cell)
            if len(cellsWithPair) == 2:
                for celll in cells:
                    if not celll in cellsWithPair:
                        if pair[0] in self.notation[celll]:
                            self.notation[celll].remove(pair[0])
                        if pair[1] in self.notation[celll]:
                            self.notation[celll].remove(pair[1])

        

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
        moves = []
        for x in range(9):
            for y in range(9):
                if self.notation[(x, y)] != [None]:
                    self.notation[(x, y)] = self.getPossibleValues((x, y))

        for y in range(9):
            self.findNakedPairs(self.game.getRow((0, y)))
            self.findNakedPairs(self.game.getColumn((x, 0)))

        for anchor in self.game.quadrantAnchors:
            self.findNakedPairs(self.game.getQuadrant(anchor))

        moves += [
            (cell, v[0]) 
            for cell, v in self.notation.items() 
            if self.notation[cell] != [None] and len(v) == 1          
        ] # check for a cell which only has 1 possibility
        
        for y in range(9):
            moves += self.findHiddenSingles(self.game.getRow((0, y)))
        
        for x in range(9):
            moves += self.findHiddenSingles(self.game.getColumn((x, 0)))

        for anchor in self.game.quadrantAnchors:
            moves += self.findHiddenSingles(self.game.getQuadrant(anchor))

        for m in moves:
            self.game.addDigit(m[0], m[1])

        self.game.solved = not None in [self.game.getValue(v) for v in self.game.grid]
        return self.game.filledCells()
