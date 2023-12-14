from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from car_agent import CarAgent
from road_space_agent import RoadSpaceAgent
from road import Road
from position import Position


#!
# \file network_model.py
# \brief A class representing the road network model.
class NetworkModel(Model):

    #!
    # \brief Constructor for the NetworkModel class.
    # \param N The number of agents.
    # \param width The width of the grid.
    # \param height The height of the grid.
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.running = True

        # Create the road
        self.road : Road = Road(2, Position(0, 0), Position(17, 14), [Position(10,14)])
        self.road.build_road()

        # Create scheduler and assign it to the model
        self.schedule = RandomActivation(self)

        # Create road marking agents
        for i, position in enumerate(self.road.road_cells):
            a = RoadSpaceAgent(i + 10000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (position.x, position.y))

        # Create car agents
        for i in range(self.num_agents):
            a = CarAgent(i, self)
            position : Position = self.road.road_cells[i]
            self.schedule.add(a)
            self.grid.place_agent(a, (position.x, position.y))


    #!
    # \brief Creates the roads of the network.
    def create_roads(self):
        self.road : Road = Road(1, Position(0, 0), Position(10, 10))
        self.road.build_road()

    #!
    # \brief Executes the steps of the agents of the model.
    def step(self):
        self.schedule.step()
