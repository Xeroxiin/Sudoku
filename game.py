
import random, json

class Cell:
    def __init__(self):
        self.locked = False
        self.value = None


class Sudoku:
    def __init__(self):
        self.grid = {}
        self.solved = False

        self.quadrantAnchors = [
            (2, 2), (5, 2), (8, 2),
            (2, 5), (5, 5), (8, 5),
            (2, 8), (5, 8), (8, 8)
        ]

        self.initial()

    def initial(self):
        for x in range(9):
            for y in range(9):
                self.grid[(x, y)] = Cell()
        self.loadGame()

    def isCellLocked(self, cell):
        return self.grid[cell].locked

    def loadGame(self):
        loadableGames = json.loads(open('startPoints.json').read())
        g = loadableGames[1]#random.choice(loadableGames)
        for i in g:
            self.grid[(i[0], i[1])].value = i[2]
            self.grid[(i[0], i[1])].locked = True
    
    def getQuadrant(self, coordinate): # coordinates
        xQuads = [3*(coordinate[0]//3) + n for n in range(3)]
        yQuads = [3*(coordinate[1]//3) + n for n in range(3)]
        return [(x, y) for x in xQuads for y in yQuads] 

    def getRow(self, coordinate):
        x, y = coordinate
        return [(i, y) for i in range(9)]

    def getColumn(self, coordinate):
        x, y = coordinate
        return [(x, i) for i in range(9)]

    def getValue(self, coordinate):
        return self.grid[coordinate].value

    def addDigit(self, coordinate, value):
        self.grid[coordinate].locked = True
        self.grid[coordinate].value = value
        #print(f'Cell ({coordinate[0]}, {coordinate[1]}) became {value}')

    def sanityCheck(self):
        #check rows / y
        for row in [self.getRow((0, row)) for row in range(9)]:
            if len(set([self.getValue(x) for x in row])) != 9:
                # failed
                return False
            
        #check columns / x
        for column in [self.getColumn((column, 0)) for column in range(9)]:
            if len(set([self.getValue(x) for x in column])) != 9:
                # failed
                return False
        #check quads
        for quad in [self.getQuadrant(x) for x in self.quadrantAnchors]:
            if len(set([self.getValue(x) for x in quad])) != 9:
                return False
        return True

    def showState(self):
        s = f'{"=" * 41}\n'
        for y in range(9):          
            s = f'{s}||'
            for x in range(9):    
                s = f'{s} {self.grid[(x, y)].value or " "}'
                if (x+1)%3 == 0:
                    s = f'{s} ||'
                else:
                    s = f'{s}  '
            if (y+1)%3 == 0:
                s = f'{s}\n{"=" * 41}\n'
            else:
                s = f'{s}\n{"-" * 41}\n'
        return s
            