from mesa import Model
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

import networkx as nx

from car_agent import CarAgent
from road_space_agent import RoadSpaceAgent
from road import Road
from position import Position
from node import Node


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
        self.roads = []
        self.G = nx.Graph()
        self.grid = NetworkGrid(self.G)
        self.running = True

        # Create scheduler and assign it to the model
        self.schedule = RandomActivation(self)

        # Create road marking agents
        #for i, position in enumerate(self.road.road_cells):
            #a = RoadSpaceAgent(i + 10000, self)
            #self.schedule.add(a)
            #self.grid.place_agent(a, (position.x, position.y))

        # Create car agents
        #for i in range(self.num_agents):
            #a = CarAgent(i, self)
            #position : Position = self.road.road_cells[i]
            #self.schedule.add(a)
            #self.grid.place_agent(a, (position.x, position.y))


    #!
    # \brief Creates the roads of the network.
    def create_road(self, start_point : Node, end_point : Node, no_lanes : int, inflection_points : list[Node] = []):
        self.roads.append(Road(no_lanes, start_point, end_point, inflection_points))

    #create a node and place it on the grid
    def create_node(self, id : int, type : int, position : Position):
        self.node = Node(id, type, position)


    #!
    # \brief Executes the steps of the agents of the model.
    def step(self):
        self.schedule.step()
