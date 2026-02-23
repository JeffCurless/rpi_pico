#
# Test setup for developing a Generative Alorithm for walking a maze
#

START = 'A'
STOP  = 'B'

possibleMoves = ['N','S', 'E', "W"]

MAX_GENERATIONS = 1000
MAX_POPULATION  = 100
MUTATION_RATE   = 0.01

maze1 = [
        ['#','#','#','#','#','#','#','#','#','#'],
        ['#','#','#','#','#',' ',' ',' ','B','#'],
        ['#','#','#','#','#',' ','#','#','#','#'],
        ['#','#','#','#','#',' ','#','#','#','#'],
        ['#','#','#','#','#',' ','#','#','#','#'],
        ['#','#','#','#','#',' ','#','#','#','#'],
        ['#','#','#','#','#',' ','#','#','#','#'],
        ['#',' ',' ',' ',' ',' ','#','#','#','#'],
        ['#','A','#','#','#','#','#','#','#','#'],
        ['#','#','#','#','#','#','#','#','#','#']
        ]

currentX = -1
currentY = -1
population = []


#
# findMazeItem - This function is used to locate an item with the maze, it is used
# for finding the coordinates of the start and stop locations
#
def findMazeItem( maze, item  ):
    for y in range( len( maze ) ):
        for x in range( len( maze[y] ) ):
            if maze[y][x] == item :
                return y, x
    return -1, -1

#
# printMaze - This function is used to print out the maze in its current state
#
def printMaze( maze ):
    for row in maze:
        for item in row:
            print( item, end = "" )
        print( "" )

#
# Some test functions
#
def testMaze1():
    starty, startx = findMazeItem( maze1, START )
    stopy,stopx = findMazeItem( maze1, STOP )
    if starty == 8 and startx == 1:
        if stopy == 1 and stopx == 8:
            return True
    return False

    print( "Error, maze does not start or stop where it is supposed to!" )

#
# Create an initial population of possible moves.... 
#
def createInitialPopulation():
    return population

#  
# initializeSystem - Generate an initial population, and setup out starting 
# point etc.
#
def initializeSystem( maze ):
    global currentY, currentX
    currentY, currentX = findMazeItem( maze1, START )
    createInitialPopulation()

#
# multateSingle - Mutate a single indivdual
#
def mutateSingle( individual ):
    return individual

#
# fixness - Determine the fitness of a single indivual command set
#
def fitness( individual ):
    return 0

#
# selectParents - Given a population, select the parents.  Note in order
# to do this properly, you will probably want to sort them by fitness and retain
# the current best possible matches.
#
def selectParents( population ):
    return population
#
# reproduceAndMutate - This routine takes the population passed in and reproduces a new population, and
# performs needed mutations based off of the mutation probabilities
#
def reproduceAndMutate( population ):
    return population

#
# determineSolution - Check to see if the existing population contains a solution or not
#
def determineSolution( population ):
    return None

#
#
#
#
if not testMaze1():
    print( "Error, maze does not start or stop where it is supposed to!" )

printMaze( maze1 )
initializeSystem( maze1 )
for generation in range( MAX_GENERATIONS ):
    solution = determineSolution( population )
    if solution != None:
        print( f"Solution to maze found, solution is : {solution}" )
    else:
        population = selectParents( population )
        population = reproduceAndMutate( population )

if generation > MAX_GENERATIONS:
    print( f"Reached {MAX_GENERATIOS} and could not find a solution!" )

