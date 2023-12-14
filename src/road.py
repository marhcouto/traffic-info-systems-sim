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
    # \brief Adds a cell to the round (the cell of the main lane 
    # and of the other lanes).
    # \param point The point of the cell.
    # \param lanes The number of lanes.
    # \param horizontal Whether the road's horizontal displacement
    # is greater than the vertical displacement (displacement between points).
    def _add_cells(self, point : Position, lanes : int, horizontal : bool = True):
        self._road_cells.append(point)
        x_increment : int = 0 if horizontal else 1
        y_increment : int = 1 if horizontal else 0

        # Put cells on one side of the road
        for i in range(1, lanes, 2):
            cell : Position = Position(point.x - x_increment * i, point.y - y_increment * i)
            if not cell.is_negative():
                self._road_cells.append(cell)

        # Put cells on the other side of the road
        for i in range(2, lanes, 2):
            cell : Position = Position(point.x + x_increment * i, point.y + y_increment * i)
            if not cell.is_negative():
                self._road_cells.append(cell)

    
    #!
    # \brief Creates the limit points of the road.
    def build_road(self):

        points_to_reach : list[Position] = self._inflection_points
        points_to_reach.append(self._end_point)
        
        current_point : Position = self._start_point

        for next_checkpoint in points_to_reach:
            step_counter : int = 0
            direction_vector = next_checkpoint - current_point
            # Whether the road's horizontal displacement is greater than 
            #the vertical displacement (displacement between points).
            horizontal : bool = abs(direction_vector.x) > abs(direction_vector.y)
            while current_point != next_checkpoint:
                # Add current point and curresponding cells for lanes
                self._add_cells(current_point, self._no_lanes, horizontal)

                # Check if next point is one cell away
                if current_point.dist(next_checkpoint) < 2:
                    current_point = next_checkpoint
                    self._add_cells(current_point, self._no_lanes, horizontal)
                    break

                # Next point (Greedy Search)
                adjacent_points : list[Position] = current_point.adjacent()
                adjacent_distances : list[float] = [adjacent_point.dist(next_checkpoint) for adjacent_point in adjacent_points]
                current_point = adjacent_points[adjacent_distances.index(min(adjacent_distances))]
                
                # Old methodology
                # movement = Movement(next_checkpoint - current_point)
                # increment : Position = movement.get_increment(step_counter) # Calculate increment
                # current_point = Position(current_point.x, current_point.y) + increment

                step_counter += 1

            current_point : Position = next_checkpoint

    @property
    def road_cells(self):
        return self._road_cells
    
    @road_cells.setter
    def road_cells(self, value : list[Position]):
        self._road_cells = value


        
        
