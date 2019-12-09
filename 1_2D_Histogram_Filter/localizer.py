import pdb
from helpers import normalize, blur

#initialize the initial belief
def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1.0 / area
    beliefs = []
    #go through the beliefs and give its value
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

#according to the sensed color and update beliefs
def sense(color, grid, beliefs, p_hit, p_miss):
    new_beliefs = []
    #
    # TODO - implement this in part 2
    #
    #go throught all the beliefs to update beliefs
    for i in range(len(grid)):
        row =[]
        for j in range(len(grid[0])):
            if(grid[i][j] == color):
                row.append(beliefs[i][j]* p_hit)
            else:
                row.append(beliefs[i][j]* p_miss)
        new_beliefs.append(row)
    #normalize beliefs
    new_beliefs = normalize(new_beliefs)
    return new_beliefs

#move and update the beliefs
def move(dy, dx, beliefs, blurring):
    #get the world size
    height = len(beliefs)
    width = len(beliefs[0])
    #creat a new belife grid
    new_G = [[0.0 for i in range(width)] for j in range(height)]
    #go through the original belief
    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            #calculate new position
            new_i = (i + dy) % height
            new_j = (j + dx) % width
            #pdb.set_trace()
            #update beliefs
            new_G[int(new_i)][int(new_j)] = cell
    #movement uncertainty
    return blur(new_G, blurring)