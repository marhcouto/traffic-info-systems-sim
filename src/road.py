from position import Position
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
    def __init__(self, no_lanes : int, start_point : Position, end_point : Position, inflection_points : list[Position] = []):
        
        self._start_point : Position = start_point
        self._end_point : Position = end_point
        self._no_lanes : int = no_lanes
        self._inflection_points : list[Position] = inflection_points
        self._road_cells : list[Position] = [] # Cell coordinates

    
    #!
    # \brief Crates the limit points of the road.
    def build_road(self):

        points_to_reach : list[Position] = self._inflection_points
        points_to_reach.append(self._end_point)
        
        current_point : Position = self._start_point

        for next_checkpoint in points_to_reach:
            step_counter : int = 0
            while current_point != next_checkpoint:
                # Lanes thingy
                self._road_cells.append(current_point)
                movement = Movement(next_checkpoint - current_point)
                if current_point.dist(next_checkpoint) < 2: # When one cell away, add next point
                    current_point = next_checkpoint
                    self._road_cells.append(current_point)
                    break
                increment : Position = movement.get_increment(step_counter) # Calculate increment
                current_point = Position(current_point.x, current_point.y) + increment
                step_counter += 1

            current_point : Position = next_checkpoint

    @property
    def road_cells(self):
        return self._road_cells
    
    @road_cells.setter
    def road_cells(self, value : list[Position]):
        self._road_cells = value


        
        
