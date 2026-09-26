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

        moves += [
            (cell, v[0]) 
            for cell, v in self.notation.items() 
            if len(v) == 1 and 
            not self.game.isCellLocked(cell) and
            not v[0] in [self.game.getValue(x) for x in self.game.getRow(cell)] and
            not v[0] in [self.game.getValue(x) for x in self.game.getColumn(cell)] and
            not v[0] in [self.game.getValue(x) for x in self.game.getQuadrant(cell)]            
        ]
        for m in moves:
            self.game.addDigit(m[0], m[1])

        self.game.solved = not None in [self.game.getValue(v) for v in self.game.grid]
        return self.game.filledCells()
