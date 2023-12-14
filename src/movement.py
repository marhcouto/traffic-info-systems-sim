import copy

from position import Position

## DEPRECATED

#!
# \file movement.py
# \brief A class representing a movement, used to decide the next positions.
# It encodes the logic behind obtaining an increment to a position
# given a vector that denotes the direction and the already travelled distance,
# given by the step counter.
class Movement:

    #!
    # \brief A dictionary of movements and their corresponding 
    # increment vectors when sliding.
    slide_movements : dict[str, Position] = {
        "north" : Position(0, 1),
        "south" : Position(0, -1),
        "east" : Position(1, 0),
        "west" : Position(-1, 0),
        "northeast" : Position(1, 1),
        "northwest" : Position(-1, 1),
        "southeast" : Position(1, -1),
        "southwest" : Position(-1, -1)
    }

    #!
    # \brief Constructor for the Movement class.
    # \param vector The vector of the movement.
    # It is the vector between the start point and the end point.
    def __init__(self, vector : Position):
        self._vector : Position = vector
        self._type : str = "north" if vector.y > 0 and vector.x == 0 else \
            "south" if vector.y < 0 and vector.x == 0 else \
            "east" if vector.x > 0 and vector.y == 0 else \
            "west" if vector.x < 0 and vector.y == 0 else \
            "northeast" if vector.y > 0 and vector.x > 0 else \
            "northwest" if vector.y > 0 and vector.x < 0 else \
            "southeast" if vector.y < 0 and vector.x > 0 else \
            "southwest"
        self._slide_rate : int = 1 if abs(vector.y) == abs(vector.x) \
            else 0 if (abs(vector.y) == 0 or abs(vector.x) == 0) \
            else abs(vector.y) // abs(vector.x) \
                if abs(vector.x) < abs(vector.y) \
              else abs(vector.x) // abs(vector.y)
        

    #!
    # \brief Get the increment of the movement.
    # The increment is the vector that is added to the current position
    #  to get closer to the next checkpoint position.
    # \param step_counter The counter of the slide (how many steps were taken)
    # \return The increment of the movement.
    def get_increment(self, step_counter : int):
        increment : Position = copy.copy(Movement.slide_movements[self._type])
        if self._slide_rate == 0 or step_counter % self._slide_rate == 0: 
            return increment
        elif abs(self._vector.x) > abs(self._vector.y):
            increment.y = 0
        else:
            increment.x = 0
        return increment
        
    
    @property
    def vector(self):
        return self._vector
    
    @vector.setter
    def vector(self, value : Position):
        self._vector : Position = value


    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value : str):
        self._type : str = value


    @property
    def slide_rate(self):
        return self._slide_rate
    
    @slide_rate.setter
    def slide_rate(self, value : int):
        self._slide_rate : int = value

