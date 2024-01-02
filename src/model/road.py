from model.node import Node


#!
# \file road.py
# \brief A class representing a road.
class Road:

    #!
    # \brief Constructor for the Road class.
    # \param no_lanes The number of lanes on the road.
    # \param start_point The starting point of the road.
    # \param end_point The end point of the road.
    # \param inflection_points A list of inflection points on the road.
    def __init__(self, start_point : Node, end_point : Node, capacity: int):
        self._start_point : Node = start_point
        self._end_point : Node = end_point
        self.capacity : int = capacity
        
        
