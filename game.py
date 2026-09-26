
import random, json

class Cell:
    def __init__(self):
        self.locked = False
        self.value = None


class Sudoku:
    def __init__(self):
        self.grid = {}
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
        print(f'Cell ({coordinate[0]}, {coordinate[1]}) became {value}')

    def showState(self, highlight=None):
        s = f'{"-" * 38}\n'
        for y in range(9):          
            s = f'{s}|'
            for x in range(9):      
                if highlight and (x, y) == highlight:
                    s = f'{s} x |'
                else:
                    s = f'{s} {self.grid[(x, y)].value or " "} |'
            s = f'{s}\n{"-" * 38}\n'
        return s
            