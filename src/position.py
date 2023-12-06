import math

#!
# \file position.py
# \brief A class representing a position.
class Position:

    #!
    # \brief Constructor for the Position class.
    # \param x The x coordinate of the position.
    # \param y The y coordinate of the position.
    def __init__(self, x : int, y : int):
        self._x : int = x
        self._y : int = y


    @property
    def x(self):
        return self._x
    

    @x.setter
    def x(self, value : int):
        self._x : int = value

    
    @property
    def y(self):
        return self._y
    

    @y.setter
    def y(self, value : int):
        self._y : int = value

    #!
    # \brief Calculates the distance between two positions.
    # \param other The other position.
    # \return The euclidian distance between the two positions.
    def dist(self, other) -> float:
        return math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)

    
    def __eq__(self, other) -> bool:
        return self._x == other._x and self._y == other._y


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    #!
    # \brief Calculator vector from other to self.
    # \param other The other position.
    # \return The vector from other to self.
    def __sub__(self, other):
        return Position(self._x - other._x, self._y - other._y)
    
    def __str__(self):
        return "(" + str(self._x) + ", " + str(self._y) + ")"
    
    #!
    # \brief Sums vector other to position self.
    def __add__(self, other):
        return Position(self._x + other._x, self._y + other._y)