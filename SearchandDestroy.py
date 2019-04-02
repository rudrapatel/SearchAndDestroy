import random

class node:
        # Function to assign the false negative value based on the terrain
        def assignFalseNegative(self, t):
                if(t == 0): 
                        self.falseNegative = 0.1
                elif(t == 1): 
                        self.falseNegative = 0.3
                elif(t == 2):
                        self.falseNegative = 0.7
                else:
                        self.falseNegative = 0.9
                
        # Set as target
        def assignTarget(self):
                self.isTarget = True

        # Un-set target for Question 2
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

# Get Target's neighbors for Question 2
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

# Calculate the manhattan distance from current cell to proposed next step cell. This works as each move has a value of 1 'action'
def getActions(startX, startY, endX, endY):
    
    return abs(endX - startX) + abs (endY - startY)

# Initialize as well as set the target in a 50x50 grid
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
                        
        targetRow = random.randint(0,49)                # Randomly select a row
        targetCol = random.randint(0,49)                # Randomly select a column
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


# The selection process for Rule 1 for both questions, the neighborENV signifies whether this is being called from question 1 or question 2

def selectCellRule1(grid, neighborENV = None):
        q = []
        q.append(grid[0][0])
        for i in range(0,len(grid)):
                for j in range(0,len(grid)):
                        if i == 0 and j == 0:
                                continue
                        if not neighborENV == None and not grid[i][j].terrain in neighborENV: # for problem 2 to only look at the cells whose terrain is the one specified by where the target moved
                                continue
                        if grid[i][j].priorBelief > q[0].priorBelief: # select the one with the highest priorBelief
                                q.clear()
                                q.append(grid[i][j])
                        elif grid[i][j].priorBelief == q[0].priorBelief: # same value of prior belief, hence we append them to the array and then select one at random
                                q.append(grid[i][j])
                                
        
        indexOfRandomCell = random.randint(0, len(q)-1)
        return q[indexOfRandomCell]

# Selection process for Rule 2, neighborENV as well highest belief behaves the same as selectRule1
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

# Slection for problem 4 - we tackle the problem of moving actions such that we divide the value of prior belief by the total number of 'move' actions to get a better understanding of the total number of moves required to move to a different cell
def selectCellRule4(grid, currentCell, neighborENV = None):
    q = list()
    q.append(grid[0][0])
    actions = list()
    if (currentCell.row == 0 and currentCell.col == 0):
        actions.append(1)
    else:
        dist = getActions(currentCell.row, currentCell.col, 0, 0) # get the number of actions required to move to the cell
        actions.append(dist)
    for i in range(0,len(grid)):
        for j in range(0,len(grid)):
            if (i == currentCell.row and j == currentCell.col) :
                continue
            if not neighborENV == None and not grid[i][j].terrain in neighborENV: # for problem 2 to only look at the cells whose terrain is the one specified by where the target moved
                continue

            dist = getActions(currentCell.row, currentCell.col, grid[i][j].row, grid[i][j].col) # get the number of actions required to move to the cell
            if (grid[i][j].priorBelief * (1 - grid[i][j].falseNegative))/dist > (q[0].priorBelief * (1 - q[0].falseNegative))/actions[0]:
                q.clear()
                actions.clear()
                q.append(grid[i][j])
                actions.append(dist)

            elif (grid[i][j].priorBelief * (1 - grid[i][j].falseNegative))/dist == (q[0].priorBelief * (1 - q[0].falseNegative))/actions[0]: # similar behavior to previous select rules
                q.append(grid[i][j])
                actions.append(dist)
                            
    
    indexOfRandomCell = random.randint(0, len(q)-1)
    return q[indexOfRandomCell], actions[indexOfRandomCell]

# the main driver functions which slects which rule/problem to execute
def FindTarget(grid , x, currTarget = None):

        if x == 1:                                                              # Question 1 Rule 1
                randomCell = selectCellRule1(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        randomCell = selectCellRule1(grid)

                print("Number of iterations using Rule 1: " + str(iteration))
                return randomCell

        elif x == 2:                                                            # Question 1 Rule 2
                randomCell = selectCellRule2(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        randomCell = selectCellRule2(grid)

                print("Number of iterations using Rule 2: " + str(iteration))
                return randomCell
        elif x == 4:                                                            # Question 1 Problem 4


            randomCell, actions = selectCellRule4(grid, grid[0][0])
            iteration = 0
            while (cellIsATarget(randomCell) == False):
                iteration+=1
                randomCell, actions = selectCellRule4(grid, randomCell)
                iteration += actions

            print("Number of iterations using Problem 4: " + str(iteration))
            return randomCell
        elif x == 21:                                                           # Question 2 Rule 1
                randomCell = selectCellRule1(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        neighbors, currTarget = moveTarget(grid, currTarget) # get the new current target as well as the two terrains
                        randomCell = selectCellRule1(grid, neighbors)

                print("Number of iterations using Question 2 Rule 1: " + str(iteration))
                return randomCell

        elif x == 22:                                                           # Question 2 Rule 2
                randomCell = selectCellRule2(grid)
                iteration = 0
                while (cellIsATarget(randomCell) == False):
                        iteration+=1
                        neighbors, currTarget = moveTarget(grid, currTarget) # get the new current target as well as the two terrains
                        randomCell = selectCellRule2(grid, neighbors)

                print("Number of iterations using Question 2 Rule 2: " + str(iteration))
                return randomCell
        elif x == 24:                                                           # Question 2 Problem 4
            randomCell, actions = selectCellRule4(grid, grid[0][0])
            iteration = 0
            while (cellIsATarget(randomCell) == False):
                iteration+=1
                neighbors, currTarget = moveTarget(grid, currTarget)
                randomCell, actions = selectCellRule4(grid, randomCell, neighbors) # get the new current target as well as the two terrains
                iteration += actions

            print("Number of iterations using Question 2 Problem 4: " + str(iteration))
            return randomCell
                

# Check whether the target is here as wellas whether the false negative is applicable here
def cellIsATarget(n):
        n.numOfTimesExamined+=1
        if n.isTarget and n.falseNegative < random.random():
                return True
        n.priorBelief = n.falseNegative * n.priorBelief
        normalize()
        return False
        
# Function to normalize the probabilities
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

print("Target found using Question 2 Rule 1 at: ["+str(target2Problem1.row)+"]["+str(target2Problem1.col)+"]")
print("Target found using Question 2 Rule 2 at: ["+str(target2Problem2.row)+"]["+str(target2Problem2.col)+"]")
print("Target found using Question 2 Prob 4 at: ["+str(target2Problem4.row)+"]["+str(target2Problem4.col)+"]")