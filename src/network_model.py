from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from car_agent import CarAgent
from road import Road
from position import Position


#!
# \file network_model.py
# \brief A class representing the road network model.
class NetworkModel(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.running = True
        self.road : Road = Road(1, Position(0, 0), Position(13, 4))
        self.road.build_road()

        # Create scheduler and assign it to the model
        self.schedule = RandomActivation(self)

        # Create agents
        for i, position in enumerate(self.road.road_cells):
            a = CarAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (position.x, position.y))


    def create_roads(self):
        self.road : Road = Road(1, Position(0, 0), Position(10, 10))
        self.road.build_road()

    def step(self):
        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()