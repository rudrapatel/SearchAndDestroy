import random

class node:

        def assignFalseNegative(self, t):
                if(t == 0): 
                        self.falseNegative = 0.1
                elif(t == 1): 
                        self.falseNegative = 0.3
                elif(t == 2):
                        self.falseNegative = 0.7
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

def getActions(startX, startY, endX, endY):
    
    return abs(endX - startX) + abs (endY - startY)

def initializeGrid():
        grid = [[node for j in range(50)] for i in range(50)]
        for i in range(0,50):                           #values of t are 0,1,2 and for flat, hilly, forest and Maze_of_caves respectively.
                for j in range(0,50):
                        rand = random.random() 
                        if rand < 0.2:  
                                t = 0
                        elif rand < 0.5:
                                t = 1
                        elif rand < 0.8:
                                t = 2
                        else:
                                t = 3
                        grid[i][j] = node(i, j, t)
                        
        targetRow = random.randint(0,49)
        targetCol = random.randint(0,49)
        grid[targetRow][targetCol].assignTarget()
        print("Our Target is at : ["+str(targetRow)+"]["+ str(targetCol)+"]")
        
        if(grid[targetRow][targetCol].terrain == 0):
                print("Terrain is Flat.")
        elif(grid[targetRow][targetCol].terrain == 1):
                print("Terrain is Hilly.")
        elif(grid[targetRow][targetCol].terrain == 2):
                print("Terrain is Forest.")
        else:
                print("Terrain is Maze of caves.")
       
        return grid

def display(grid):
        for i in range(10):
                for j in range(10):
                        print(grid[i][j].terrain)


def selectCellRule1(grid):
        q = []
        q.append(grid[0][0])
        for i in range(0,len(grid)):
                for j in range(0,len(grid)):
                        if i == 0 and j == 0:
                                continue
                        if grid[i][j].priorBelief > q[0].priorBelief:
                                q.clear()
                                q.append(grid[i][j])
                        elif grid[i][j].priorBelief == q[0].priorBelief:
                                q.append(grid[i][j])
                                
        
        indexOfRandomCell = random.randint(0, len(q)-1)
        return q[indexOfRandomCell]


def selectCellRule2(grid):
        q = []
        q.append(grid[0][0])
        for i in range(0,len(grid)):
                for j in range(0,len(grid)):
                        if i == 0 and j == 0:
                                continue
                        if grid[i][j].priorBelief * (1 - grid[i][j].falseNegative) > q[0].priorBelief * (1 - q[0].falseNegative):
                                q.clear()
                                q.append(grid[i][j])
                        elif grid[i][j].priorBelief * (1 - grid[i][j].falseNegative) == q[0].priorBelief * (1 - q[0].falseNegative):
                                q.append(grid[i][j])
                                
        
        indexOfRandomCell = random.randint(0, len(q)-1)
        return q[indexOfRandomCell]

def selectCellRule4(grid, currentCell):
    q = list()
    q.append(grid[0][0])
    actions = list()
    if (currentCell.row == 0 and currentCell.col == 0):
        actions.append(1)
    else:
        dist = getActions(currentCell.row, currentCell.col, 0, 0)
        actions.append(dist)
    for i in range(0,len(grid)):
        for j in range(0,len(grid)):
            if i == currentCell.row and j == currentCell.col:
                continue
            dist = getActions(currentCell.row, currentCell.col, grid[i][j].row, grid[i][j].col)
            if (grid[i][j].priorBelief * (1 - grid[i][j].falseNegative))/dist > (q[0].priorBelief * (1 - q[0].falseNegative))/actions[0]:
                q.clear()
                actions.clear()
                q.append(grid[i][j])
                actions.append(dist)

            elif (grid[i][j].priorBelief * (1 - grid[i][j].falseNegative))/dist == (q[0].priorBelief * (1 - q[0].falseNegative))/actions[0]:
                q.append(grid[i][j])
                actions.append(dist)
                            
    
    indexOfRandomCell = random.randint(0, len(q)-1)
    return q[indexOfRandomCell], actions[indexOfRandomCell]


def FindTarget(grid , x):

        if x == 1:
                randomCell = selectCellRule1(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        randomCell = selectCellRule1(grid)

                print("Number of iterations using Rule 1: " + str(iteration))
                return randomCell

        elif x == 2:
                randomCell = selectCellRule2(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        randomCell = selectCellRule2(grid)

                print("Number of iterations using Rule 2: " + str(iteration))
                return randomCell
        elif x == 4:


            randomCell, actions = selectCellRule4(grid, grid[0][0])
            iteration = 0
            while (cellIsATarget(randomCell) == False):
                iteration+=1
                randomCell, actions = selectCellRule4(grid, randomCell)
                iteration += actions

            print("Number of iterations using Problem 4: " + str(iteration))
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
gridRule2 = grid
gridProb4 = grid

target = FindTarget(grid ,1)


targetTwo = FindTarget(gridRule2,2)

targetProblem4 = FindTarget(gridProb4, 4)
print("Target found using Rule 1 at: ["+str(target.row)+"]["+str(target.col)+"]")
print("Target found using Rule 2 at: ["+str(targetTwo.row)+"]["+str(targetTwo.col)+"]")
print("Target found using Prob 4 at: ["+str(targetProblem4.row)+"]["+str(targetProblem4.col)+"]")