import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from network_agent import NetworkAgent



class NetworkModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.G = nx.Graph()
        self.schedule = RandomActivation(self)

        # Create agents and add them to the network
        for i in range(self.num_agents):
            a = NetworkAgent(i, self)
            self.schedule.add(a)
            self.G.add_node(a)

        # Add edges to the network
        # Example: create a ring network
        for i in range(self.num_agents):
            a = self.schedule.agents[i]
            b = self.schedule.agents[(i + 1) % self.num_agents]
            self.G.add_edge(a, b)

    def step(self):
        pass