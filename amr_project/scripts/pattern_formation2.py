from itertools import permutations

def pattern(x, y): # generates all vertices of equilateral traingle based on current leader position
    
    """if num == 3:
        coords = ((x - 7, y), (x + 7, y), (x, y - 10))
    elif num == 4:
        coords = ((x - 7, y), (x + 7, y), (x, y - 7), (x, y + 7))
    elif num == 5:
        coords = ((x - 7, y), (x + 7, y), (x, y + 10), (x - 3, y - 5), (x + 3, y - 5))"""
    coords = ((x - 7, y + 3), (x + 7, y + 3), (x + 7, y - 3), (x -7, y - 3), (x, y + 10), (x, y - 10))
    
    #coords = ((x - 7, y), (x + 7, y ), (x + 6, y ), (x -6, y ), (x+5, y), (x-5, y))

    return coords


def distance(x1, y1, x2, y2): # function to calculate euclidean distance
    dist = ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)
    return dist

def who_goes_where(current, vertices, num): # each parameter contains 3 tuples of form (x, y)
    bots_dist = []
    for nums in range(num):
    	bots_dist.append(nums)
    min_dist = 0
    for i in range(num):
        bots_dist[i] = []
        for j in range(num):
            dist = distance(current[i][0], current[i][1], vertices[j][0], vertices[j][1])
            bots_dist[i].append(dist)
            if i == j:
                min_dist += dist

    costs = [] # can be removed - will be useful for debugging

    # all possible combinations of which vertex each bot shld go to

    #pairings = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    pairings = list(permutations(range(0, num)))
    min_order = pairings[0]

    for i in range(1, len(pairings)): # will chk all combinations of pairings to choose min cost one
        pairing = pairings[i]
        dist = 0
        for j in range(len(pairing)):
            dist += bots_dist[0][pairing[j]]
        # dist = bot1_distances[pairing[0]] + bot2_distances[pairing[1]] + bot3_distances[pairing[2]]
        costs.append(dist) # can be removed - will be useful for debugging
        if dist < min_dist:
            min_dist, min_order = dist, pairings[i]

    # tuple which stores the x,y coords as a tuple to which each bot shld go to (so 1st tuple is for 1st bot)
    # where_to_go = (vertices[min_order[0]], vertices[min_order[1]], vertices[min_order[2]])
    where_to_go = []
    print(min_order)
    for i in range(len(min_order)):
        where_to_go.append(vertices[min_order[i]])

    if needed:
    	return where_to_go


def delta(old_xy, new_xy):
    delta_x = new_xy[0] - old_xy[0]
    delta_y = new_xy[1] - old_xy[1]
    return (delta_x, delta_y)


def new_position(current, delta):
    new_pos_1 = (current[0][0] + delta[0], current[0][1] + delta[1])
    new_pos_2 = (current[1][0] + delta[0], current[1][1] + delta[1])
    new_pos_3 = (current[2][0] + delta[0], current[2][1] + delta[1])
    new_pos_4 = (current[3][0] + delta[0], current[3][1] + delta[1])
    new_pos_5 = (current[4][0] + delta[0], current[4][1] + delta[1])
    new_pos_6 = (current[5][0] + delta[0], current[5][1] + delta[1])

    return (new_pos_1, new_pos_2, new_pos_3, new_pos_4, new_pos_5, new_pos_6)
