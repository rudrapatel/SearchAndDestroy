import random


class node:

        def assignFalseNegative(self, t):
                if(t == 0): 
                        self.falseNegative = 0.1
                elif(t == 1): 
                        self.falseNegative = 0.7
                elif(t == 2):
                        self.falseNegative = 0.3
                else:
                        self.falseNegative = 0.9
                
        
        
        def assignTarget(self):
                self.isTarget = True
                
        def __init__(self, row, col, terrain):
                self.row = row
                self.col = col
                self.terrain = terrain
                self.assignFalseNegative(terrain)
                self.priorBelief = 0.0004
                self.isTarget = False
                self.numOfTimesExamined = 0
        
        
        




def initializeGrid():
        grid = [[node for j in range(50)] for i in range(50)]
        for i in range(0,50):
                for j in range(0,50):
                        rand = random.random() 
                        if rand < 0.2:  #values of t are 0,1,2 and for flat, hilly, forest and Maze_of_caves respectively.
                                t = 0
                        elif rand < 0.5:
                                t = 1
                        elif rand < 0.8:
                                t = 2
                        else:
                                t = 3
                        grid[i][j] = node(i, j, t)
                        
        targetRow = random.randint(0,50)
        targetCol = random.randint(0,50)
        grid[targetRow][targetCol].assignTarget()
        print("assigned value is :")
        print(targetRow)
        print(targetCol)
       
        return grid

def display(grid):
        for i in range(10):
                for j in range(10):
                        print(grid[i][j].terrain)


def selectCell(map):
        q = []
        q.append(map[0][0])
        for i in range(0,len(map)):
                for j in range(0,len(map)):
                        if i == 0 and j == 0:
                                continue
                        if map[i][j].priorBelief > q.pop(0).priorBelief:
                                q.clear()
                                q.append(map[i][j])
                        elif map[i][j].priorBelief == q.pop(0).priorBelief:
                                q.append(map[i][j])
                                

        indexOfRandomCell = random.randint(0, len(q))
        return q.pop(indexOfRandomCell)




def partOne(grid):
        
        randomCell = selectCell(grid)
        iteration = 0
        while (cellIsATarget(randomCell) == False):
                iteration+=1
                randomCell = selectCell(grid)

        print("Number of iterations: " + iteration)
        return randomCell



def cellIsATarget(n):
        n.numOfTimesExamined+=1
        if n.isTarget and n.falseNegative < random.random():
                return True
        n.priorBelief = n.falseNegative * n.priorBelief
        normalize()
        return False
        

def normalize():
        sumOfProbabilities = 0
        for i in range(0,50):
                for j in range(0,50):
                        sumOfProbabilities += grid[i][j].priorBelief
                        

        for i in range(0,50):
                for j in range(0,50):
                        grid[i][j].priorBelief = grid[i][j].priorBelief * (1 / sumOfProbabilities)


                
            
grid = initializeGrid()

target = partOne(grid)
print(target.row)
print(target.column)


