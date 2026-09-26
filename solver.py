quadrantAnchors = [
    (2, 2), (5, 2), (8, 2),
    (2, 5), (5, 5), (8, 5),
    (2, 8), (5, 8), (8, 8)
]

class Solver:
    def __init__(self, game):
        self.game = game
        self.known = game.grid
        self.notation = {}
        
        for y in range(9):
            for x in range(9):
                if self.known[(x, y)].locked == True:
                    self.notation[(x, y)] = [-1]
                else:
                    self.notation[(x, y)] = []

    def findMising(self, has):
        return [missing for missing in list(range(1, 10)) if not missing in has]

    def findOutliers(self, sets):
        specials = {}
        for c1 in sets:
            specials[c1] = self.notation[c1]
            for c2 in sets:
                if c1 != c2 and self.game.getValue(c2) in self.notation[c1]:
                    specials[c1].remove(self.game.getValue(c2))
        return specials
    
    def iterate(self):
        for anchor in quadrantAnchors:
            quadMissing = list(range(1,10))
            possibleMoves = {1: [], 2: [], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            emptyCells = []

            for cell in self.game.getQuadrant(anchor):
                if self.game.isCellLocked(cell):
                    quadMissing.remove(self.game.getValue(cell))
                else:
                    emptyCells.append(cell)


            for digit in quadMissing:
                for cell in emptyCells:
                    rowCheck = digit in [self.game.getValue(ce) for ce in self.game.getRow(cell)] # false is a pass - digit is not in the list
                    columnCheck = digit in [self.game.getValue(ce) for ce in self.game.getColumn(cell)]
                    if rowCheck == False and columnCheck == False:
                        possibleMoves[digit].append(cell)


                if len(possibleMoves[digit]) == 1:
                    self.game.addDigit(possibleMoves[digit][0], digit)
                    #print(f'Cell ({possibleMoves[digit][0][0]},{possibleMoves[digit][0][1]}) = {digit}')
                    #print(f'{digit}: {[possibleMoves[digit][0]]}')
        print(self.game.showState())
        