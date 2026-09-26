quadrantAnchors = [
    (2, 2), (5, 2), (8, 2),
    (2, 5), (5, 5), (8, 5),
    (8, 2), (8, 5), (8, 8)     
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
        movesToMake = []

        for coord, cell in self.notation.items():
            if cell == []:

                rCContent = self.game.getRow(coord[1])
                cCContent = self.game.getColumn(coord[0])
                qCContent = self.game.getQuadrant(coord[0], coord[1])

                rValue = [self.game.getValue(v) for v in rCContent]
                cValue = [self.game.getValue(v) for v in cCContent]
                qValue = [self.game.getValue(v) for v in qCContent]

                possible = self.findMising(qValue) # missing quadrant values
                for x in possible:
                    if x in rValue:
                        possible.remove(x)
                    elif x in cValue:
                        possible.remove(x)

                self.notation[coord] = possible
                #print(f'[{self.game.grid[coord].value}] ({coord[1]}, {coord[0]}) - {possible}')

        '''for coord, cell in self.notation.items():
            cellsQuad = [x for x in self.game.getQuadrant(coord[0], coord[1]) if not -1 in self.notation[x]]

            cellsRow = [x for x in self.game.getRow(coord[1]) if not -1 in self.notation[x]]

            cellsColumn = [x for x in self.game.getColumn(coord[0]) if not -1 in self.notation[x]]

            cellsCombi = cellsQuad + cellsRow + cellsColumn
            outliersCombi = self.findOutliers(cellsCombi)
            if len(outliersCombi) == 1:
                movesToMake.append(coord, outliersCombi[0])
            print(f'combi: {outliersCombi}')'''

        for anchor in quadrantAnchors:
            quadMissing = list(range(1,10))
            emptyCells = []
            for cell in self.game.getQuadrant(anchor[0], anchor[1]):
                if self.game.getValue(cell) != None:
                    # has a value assigned
                    quadMissing.remove(self.game.getValue(cell))
                else:
                    emptyCells.append(cell)
            for digit in quadMissing:
                for cell in emptyCells:
                    pass 
        
        print(movesToMake)