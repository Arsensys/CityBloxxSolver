# This code is a personal attempt to solve the
# old game called City Bloxx. 

# This code generates possible solutions given the following rules:
# 1) A city has a A * B dimension (like a 2d array)
# 2) Each array possition represents a city spot where a tower can be placed.
# 3) Exist  four tower types, each one represented by a value (2, 4, 6, 8)
#    The original game represents tower by colors as follows: Blue (2), Red (4), Green (6) and Yellow (8)
# 4) Except for the Blue tower (2), each tower requires other towers as neighbors for being builded:

#    Blue tower (2) does not require neighbors
#    Red tower (4) requires a least a Blue tower as neighbor
#    Green tower (6) requires a least a Blue tower and a Red tower as neighbors
#    Yellow tower (8) requires a least a Blue tower, a Red tower and a Green tower as neighbors

#    Required neighbors must be placed directly up, right, down or left from the tower you want to build
#    No diagonal towwer are admited as valid neighbors

# The main goal of the game is to place towers 

import pandas as pd
from random import randint

tower1_value = 2
tower2_value = 4
tower3_value = 6
tower4_value = 8

required_neighbors_by_tower = {
    tower1_value :[],
    tower2_value :[2],
    tower3_value :[2, 4],
    tower4_value :[2, 4, 6], 
}

city_rows = 0
city_cols = 0
city = []

def init_city(rows, cols):
    global city_rows, city_cols
    city_rows = rows
    city_cols = cols
    set_empty_spots(cols, rows)
    #city_iterator_random(600000, 3)
    #city_iterator_lineal_with_dependency_supplier()
    city_iterator_random_with_dependency_supplier(1000)
    print(print_city())
    print(print_city_towers_resume())
   
def print_city():
    y_labels = [' '] * city_cols
    x_labels = [' '] * city_rows
    print (pd.DataFrame(city, index=y_labels, columns=x_labels))

def print_city_towers_resume():
    resume = {}

    for row in city:
        for tower in row:
            if tower in resume:
                resume[tower] += 1
            else:
                resume[tower] = 1

    print(resume)

def set_empty_spots(cols, rows):
    global city
    city =  [[0 for i in range(cols)] for j in range(rows)] 

def city_iterator():
    global city
    for tower_type in range(2, 10, 2):
        for x_coordinate in range(city_rows):
            for y_coordinate in range(city_cols):
                if check_tower_creation_availability(tower_type, x_coordinate, y_coordinate):
                    city[x_coordinate][y_coordinate] = tower_type
        print(city)

def city_iterator_random(max_cycles, yellow_tower_expectative):
    current_cyle = 1
    yellow_tower_count = 0

    while current_cyle <= max_cycles and yellow_tower_count < yellow_tower_expectative:    
        current_cyle = current_cyle + 1
        x_coordinate = randint(0, (city_rows - 1))
        y_coordinate = randint(0, (city_cols - 1))

        for tower_type in list(range(2, 10, 2)):
            if check_tower_creation_availability(tower_type, x_coordinate, y_coordinate) and get_tower_type(x_coordinate, y_coordinate) != 8:
                create_tower(tower_type, x_coordinate, y_coordinate)
                
                if tower_type == 8:
                    yellow_tower_count = (yellow_tower_count + 1)
                pass

def city_iterator_lineal_with_dependency_supplier():
    global city

    for tower_type in range(2, 10, 2):
        for x_coordinate in range(city_rows):
            for y_coordinate in range(city_cols):
                if check_tower_creation_availability(tower_type, x_coordinate, y_coordinate):
                    create_tower(tower_type, x_coordinate, y_coordinate)
                else:
                    tower_has_dependencies_spots = check_tower_dependencies_supply_availability(tower_type, x_coordinate, y_coordinate)

                    if tower_has_dependencies_spots[0]:
                        tower_dependencies = calculate_required_tower_dependencies(tower_type, tower_has_dependencies_spots[1])
                        
                        for dependency in tower_dependencies:
                            tower_val = dependency[0]
                            tower_x = dependency[1]
                            tower_y = dependency[2]
                            city[tower_x][tower_y] = tower_val

def city_iterator_random_with_dependency_supplier(iterations):
    global city
    
    for tower_type in range(iterations):
        x_coordinate = randint(0, (city_rows - 1))
        y_coordinate = randint(0, (city_cols - 1))

        for tower_type in range(2, 10, 2):
           
            if check_tower_creation_availability(tower_type, x_coordinate, y_coordinate):
                create_tower(tower_type, x_coordinate, y_coordinate)
            else:
                tower_has_dependencies_spots = check_tower_dependencies_supply_availability(tower_type, x_coordinate, y_coordinate)

                if tower_has_dependencies_spots[0]:
                    tower_dependencies = calculate_required_tower_dependencies(tower_type, tower_has_dependencies_spots[1])
                    
                    for dependency in tower_dependencies:
                        tower_val = dependency[0]
                        tower_x = dependency[1]
                        tower_y = dependency[2]
                        city[tower_x][tower_y] = tower_val
              
# Allows get a tower neighbors given its coordinates
def get_tower_neighbors(tower_x_coordinate, tower_y_coordinate):
    neighbors = []

    # up neighbor
    if tower_x_coordinate == 0 :
        neighbors.append(None)
    else:
        neighbors.append(city[tower_x_coordinate - 1][tower_y_coordinate])
    
    # right neighbor
    if tower_y_coordinate == (city_cols - 1) :
        neighbors.append(None)
    else:
        neighbors.append(city[tower_x_coordinate][tower_y_coordinate + 1])

    # down neighbor
    if tower_x_coordinate == (city_rows - 1) :
        neighbors.append(None)
    else:
        neighbors.append(city[tower_x_coordinate + 1][tower_y_coordinate])
    
    # left neighbor
    if tower_y_coordinate == 0 :
        neighbors.append(None)
    else:
        neighbors.append(city[tower_x_coordinate][tower_y_coordinate - 1])

    return neighbors

# Allows get a tower neighbors and its coordinates given the tower coordinates
def get_tower_neighbors_with_coordinates(tower_x_coordinate, tower_y_coordinate):
    neighbors = []

    # up neighbor
    if tower_x_coordinate == 0 :
        neighbors.append(None)
    else:
        neighbors.append([city[tower_x_coordinate - 1][tower_y_coordinate], tower_x_coordinate -1 , tower_y_coordinate])
    
    # right neighbor
    if tower_y_coordinate == (city_cols - 1) :
        neighbors.append(None)
    else:
        neighbors.append([city[tower_x_coordinate][tower_y_coordinate + 1], tower_x_coordinate, tower_y_coordinate + 1])

    # down neighbor
    if tower_x_coordinate == (city_rows - 1) :
        neighbors.append(None)
    else:
        neighbors.append([city[tower_x_coordinate + 1][tower_y_coordinate], tower_x_coordinate + 1, tower_y_coordinate])
    
    # left neighbor
    if tower_y_coordinate == 0 :
        neighbors.append(None)
    else:
        neighbors.append([city[tower_x_coordinate][tower_y_coordinate - 1], tower_x_coordinate, tower_y_coordinate - 1])

    return neighbors

# Allows to check the posibility to create a tower given its tower type and coordinates
def check_tower_creation_availability(tower_value, tower_x_coordinate, tower_y_coordinate):
    current_tower_neighbors = get_tower_neighbors(tower_x_coordinate, tower_y_coordinate)
    required_neighbors = required_neighbors_by_tower[tower_value]

    for required_neighbor in required_neighbors:
        try:
           current_tower_neighbors.index(required_neighbor)
        except ValueError:
            return False
    
    return True

# Allows to check the posibility to create a tower dependencies
def check_tower_dependencies_supply_availability(tower_type, tower_x_coordinate, tower_y_coordinate):
    current_tower_neighbors = get_tower_neighbors_with_coordinates(tower_x_coordinate, tower_y_coordinate)
    required_neighbors = required_neighbors_by_tower[tower_type]
    available_tower_neighbors = [spot for spot in current_tower_neighbors if spot is not None and (spot[0] < tower_type) ]
    tower_spots_are_vailable = (len(available_tower_neighbors) >= len(required_neighbors))

    return [tower_spots_are_vailable, available_tower_neighbors]

def calculate_required_tower_dependencies(tower_type, tower_arround_spots):
    required_neighbors = required_neighbors_by_tower[tower_type]
    tower_real_dependencies = []
    remaining_dependencies_spots = list(tower_arround_spots)

    for required_neighbor in required_neighbors:
        exists_neighbor = False
        
        for index, neighbor_spot in enumerate(tower_arround_spots):
            if required_neighbor == neighbor_spot[0]:
                remaining_dependencies_spots[index] = None
                exists_neighbor = True
                break
              
        if not exists_neighbor:
            tower_real_dependencies.append(required_neighbor)
        
    # Clear empty list possitons 
    remaining_dependencies_spots = [spot for spot in remaining_dependencies_spots if spot is not None]
    
    for index, real_dependency in enumerate(tower_real_dependencies):
        remaining_dependencies_spots[index][0] = real_dependency

    return remaining_dependencies_spots

def check_if_tower_spot_is_empty(tower_x_coordinate, tower_y_coordinate):
    tower_type = city[tower_x_coordinate][tower_y_coordinate]
    return (tower_type == 0)

def get_tower_type(tower_x_coordinate, tower_y_coordinate):
    return city[tower_x_coordinate][tower_y_coordinate]

def create_tower(tower_type, tower_x_coordinate, tower_y_coordinate):
     global city
     city[tower_x_coordinate][tower_y_coordinate] = tower_type

init_city(3, 3)