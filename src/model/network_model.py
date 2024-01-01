from mesa import Model
from mesa.space import NetworkGrid
from mesa.time import RandomActivation

import networkx as nx

from car_agent import CarAgent
from road_space_agent import RoadSpaceAgent
from model.road import Road
from position import Position
from model.node import Node


#!
# \file network_model.py
# \brief A class representing the road network model.
class NetworkModel(Model):

    #!
    # \brief Constructor for the NetworkModel class.
    # \param N The number of agents.
    # \param width The width of the grid.
    # \param height The height of the grid.
    def __init__(self, N, roads: list):
        self.num_agents = N
        self.G = self.create_graph(roads)
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
    def create_graph(self, roads):
        G = nx.Graph()
        i = 1
        for road in roads:
            G.add_edge(road._start_point, road._end_point, id=i, capacity=road.capacity)
            i += 1
        return G
    #!
    # \brief Executes the steps of the agents of the model.
    def step(self):
        self.schedule.step()
