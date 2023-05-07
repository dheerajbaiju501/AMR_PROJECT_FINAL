def pattern1(x, y): # generates all vertices of equilateral traingle based on current leader position
    coords = ((x - 7, y), (x + 7, y), (x, y - 10))
    return coords

def distance(x1, y1, x2, y2): # function to calculate euclidean distance
    dist = ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)
    return dist

def who_goes_where(current, vertices): # each parameter contains 3 tuples of form (x, y)
    bot1_x, bot1_y = current[0][0], current[0][1]
    bot2_x, bot2_y = current[1][0], current[1][1]
    bot3_x, bot3_y = current[2][0], current[2][1]

    # dist of each bot from each of the vertices
    bot1_distances = [distance(bot1_x, bot1_y, vertices[0][0], vertices[0][1]),
                      distance(bot1_x, bot1_y, vertices[1][0], vertices[1][1]),
                      distance(bot1_x, bot1_y, vertices[2][0], vertices[2][1])]
    bot2_distances = [distance(bot2_x, bot2_y, vertices[0][0], vertices[0][1]),
                      distance(bot2_x, bot2_y, vertices[1][0], vertices[1][1]),
                      distance(bot2_x, bot2_y, vertices[2][0], vertices[2][1])]
    bot3_distances = [distance(bot3_x, bot3_y, vertices[0][0], vertices[0][1]),
                      distance(bot3_x, bot3_y, vertices[1][0], vertices[1][1]),
                      distance(bot3_x, bot3_y, vertices[2][0], vertices[2][1])]

    costs = [] # can be removed - will be useful for debugging

    # all possible combinations of which vertex each bot shld go to
    pairings = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

    # setting min dist to 1st pairing
    min_dist = bot1_distances[0] + bot2_distances[1] + bot3_distances[2]
    min_order = pairings[0]

    for i in range(2, 6): # will chk all combinations of pairings to choose min cost one
        pairing = pairings[i]
        dist = bot1_distances[pairing[0]] + bot2_distances[pairing[1]] + bot3_distances[pairing[2]]
        costs.append(dist) # can be removed - will be useful for debugging
        if dist < min_dist:
            min_dist, min_order = dist, pairings[i]

    # tuple which stores the x,y coords as a tuple to which each bot shld go to (so 1st tuple is for 1st bot)
    where_to_go = (vertices[min_order[0]], vertices[min_order[1]], vertices[min_order[2]])

    return where_to_go


