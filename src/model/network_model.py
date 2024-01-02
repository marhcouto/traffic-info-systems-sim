from mesa import Model
from mesa.time import RandomActivation

import networkx as nx

from model.network_node import NetworkNode
from model.route_agent import RouteAgent


#!
# \file network_model.py
# \brief A class representing the road network model.
class NetworkModel(Model):

    #!
    # \brief Constructor for the NetworkModel class.
    def __init__(self):
        # self.running = True

        self.routes : list[RouteAgent] = []
        self.nodes : list[NetworkNode] = []
        self.schedule = RandomActivation(self)
        self.G = None

        self.nodes.append(NetworkNode(0, self))
        self.nodes.append(NetworkNode(1, self))
        self.nodes.append(NetworkNode(2, self))
        self.nodes.append(NetworkNode(3, self))
        self.routes.append(RouteAgent(4, self, 40, 40, 40, 0.15, 4, self.nodes[0], self.nodes[1]))
        self.routes.append(RouteAgent(5, self, 40, 40, 40, 0.15, 4, self.nodes[0], self.nodes[2]))
        self.routes.append(RouteAgent(6, self, 40, 40, 40, 0.15, 4, self.nodes[1], self.nodes[3]))
        self.routes.append(RouteAgent(7, self, 40, 40, 40, 0.15, 4, self.nodes[2], self.nodes[3]))
        self.G = self.create_graph(self.routes)

        
    #!
    # \brief Creates the roads of the network and schedules agents.
    def create_graph(self, routes : list[RouteAgent]):
        G = nx.Graph()
        for route in routes:
            if route.origin is None or route.destination is None:
                continue
            if not G.has_node(route.origin):
                self.schedule.add(route.origin)
                G.add_node(route.origin)
            if not G.has_node(route.destination):
                self.schedule.add(route.destination)
                G.add_node(route.destination)
            G.add_edge(route.origin, route.destination, capacity = route.capacity)
            self.schedule.add(route)

        return G


    #!
    # \brief Executes the steps of the agents of the model.
    def step(self):
        self.schedule.step()
