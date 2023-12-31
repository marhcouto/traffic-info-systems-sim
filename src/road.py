from position import Position
from node import Node
from movement import Movement


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
    def __init__(self, no_lanes : int, start_point : Node, end_point : Node, inflection_points : list[Node] = []):
        
        self._start_point : Node = start_point
        self._end_point : Node = end_point
        self._no_lanes : int = no_lanes
        self._inflection_points : list[Node] = inflection_points

        
        
