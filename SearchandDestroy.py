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

        def unassigntarget(self):
            self.isTarget = False   

        def __init__(self, row, col, terrain):
                self.row = row
                self.col = col
                self.terrain = terrain
                self.assignFalseNegative(terrain)
                self.priorBelief = 0.0004
                self.isTarget = False
                self.numOfTimesExamined = 0

def getNeighbors(node, dim):
    x,y = node
    if x == 0 and y == 0 :
        return [(0,1), (1,0)]
    elif x == dim-1 and y ==0:
        return [(x-1, y), (x, y+1)]
    elif x == 0 and y == dim-1:
        return [(x, y-1), (x+1, y)]
    elif x == dim - 1 and y == dim-1:
        return [(x, y-1), (x-1, y)]
    elif x == 0:
        return [(x, y-1), (x, y+1), (x+1, y)]
    elif x == dim-1:
        return [(x, y-1), (x, y+1), (x-1, y)]
    elif y == 0:
        return [(x-1, y), (x, y+1), (x+1, y)]
    elif y == dim-1:
        return [(x, y-1), (x-1, y), (x+1, y)]
    else:
        return [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]

# Here we get the neighbors, then at random choose one of the them to be the target and then return the terrains as well as the currentTargent 
def moveTarget(grid, currTarget):
    neigh = getNeighbors(currTarget, 50)
    x, y = currTarget
    grid[x][y].unassigntarget()
    rand = random.randint(0, len(neigh) - 1)
    nX, nY = neigh[rand]
    grid[nX][nY].assignTarget()
    return [grid[x][y].terrain, grid[nX][nY].terrain], (nX, nY)

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
       
        return grid, (targetRow, targetCol)

def display(grid):
        for i in range(10):
                for j in range(10):
                        print(grid[i][j].terrain)


def selectCellRule1(grid, neighborENV = None):
        q = []
        q.append(grid[0][0])
        for i in range(0,len(grid)):
                for j in range(0,len(grid)):
                        if i == 0 and j == 0:
                                continue
                        if not neighborENV == None and not grid[i][j].terrain in neighborENV: # for problem 2 to only look at the cells whose terrain is the one specified by where the target moved
                                continue
                        if grid[i][j].priorBelief > q[0].priorBelief:
                                q.clear()
                                q.append(grid[i][j])
                        elif grid[i][j].priorBelief == q[0].priorBelief:
                                q.append(grid[i][j])
                                
        
        indexOfRandomCell = random.randint(0, len(q)-1)
        return q[indexOfRandomCell]


def selectCellRule2(grid, neighborENV = None):
        q = []
        q.append(grid[0][0])
        for i in range(0,len(grid)):
                for j in range(0,len(grid)):
                        if i == 0 and j == 0:
                                continue
                        if not neighborENV == None and not grid[i][j].terrain in neighborENV: # for problem 2 to only look at the cells whose terrain is the one specified by where the target moved
                                continue
                        if grid[i][j].priorBelief * (1 - grid[i][j].falseNegative) > q[0].priorBelief * (1 - q[0].falseNegative):
                                q.clear()
                                q.append(grid[i][j])
                        elif grid[i][j].priorBelief * (1 - grid[i][j].falseNegative) == q[0].priorBelief * (1 - q[0].falseNegative):
                                q.append(grid[i][j])
                                
        
        indexOfRandomCell = random.randint(0, len(q)-1)
        return q[indexOfRandomCell]

def selectCellRule4(grid, currentCell, neighborENV = None):
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
            if (i == currentCell.row and j == currentCell.col) :
                continue
            if not neighborENV == None and not grid[i][j].terrain in neighborENV: # for problem 2 to only look at the cells whose terrain is the one specified by where the target moved
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


def FindTarget(grid , x, currTarget = None):

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
        if x == 21:
                randomCell = selectCellRule1(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        neighbors, currTarget = moveTarget(grid, currTarget)
                        randomCell = selectCellRule1(grid, neighbors)

                print("Number of iterations using Question 2 Rule 1: " + str(iteration))
                return randomCell

        elif x == 22:
                randomCell = selectCellRule2(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        neighbors, currTarget = moveTarget(grid, currTarget)
                        randomCell = selectCellRule2(grid, neighbors)

                print("Number of iterations using Question 2 Rule 2: " + str(iteration))
                return randomCell
        elif x == 24:
            randomCell, actions = selectCellRule4(grid, grid[0][0])
            iteration = 0
            while (cellIsATarget(randomCell) == False):
                iteration+=1
                neighbors, currTarget = moveTarget(grid, currTarget)
                randomCell, actions = selectCellRule4(grid, randomCell, neighbors)
                iteration += actions

            print("Number of iterations using Question 2 Problem 4: " + str(iteration))
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


                
            
grid, realTarget = initializeGrid()
gridRule2 = grid
gridProb4 = grid
grid2Prob1 = grid
grid2Prob2 = grid
grid2Prob4 = grid

realTarget1 = realTarget
realTarget2 = realTarget
realTarget4 = realTarget

target = FindTarget(grid ,1)
targetTwo = FindTarget(gridRule2,2)
targetProblem4 = FindTarget(gridProb4, 4)
target2Problem1 = FindTarget(grid2Prob1, 21, realTarget1)
target2Problem2 = FindTarget(grid2Prob2, 22, realTarget2)
target2Problem4 = FindTarget(grid2Prob4, 24, realTarget4)
print("Target found using Rule 1 at: ["+str(target.row)+"]["+str(target.col)+"]")
print("Target found using Rule 2 at: ["+str(targetTwo.row)+"]["+str(targetTwo.col)+"]")
print("Target found using Prob 4 at: ["+str(targetProblem4.row)+"]["+str(targetProblem4.col)+"]")

print("Target found using Question 2 Prob 1 at: ["+str(target2Problem1.row)+"]["+str(target2Problem1.col)+"]")
print("Target found using Question 2 Prob 2 at: ["+str(target2Problem2.row)+"]["+str(target2Problem2.col)+"]")
print("Target found using Question 2 Prob 4 at: ["+str(target2Problem4.row)+"]["+str(target2Problem4.col)+"]")