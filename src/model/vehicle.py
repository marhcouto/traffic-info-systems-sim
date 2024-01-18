from random import random

import networkx as nx
from mesa import Agent


# Vehicle class
# Represents a vehicle agent in the network
class Vehicle(Agent):

    # Constructor for the Vehicle class
    # Params:
    #   unique_id: unique id of the agent
    #   model: the model the agent is in
    #   prob_gps: probability of the vehicle following the GPS
    def __init__(self, unique_id, model, prob_gps):
        super().__init__(unique_id, model)
        self.prob_gps = prob_gps

        self.travel_time = 0  # Time the vehicle has been in the network
        self.pos = 0  # The route the vehicle is in, intially set to 0
        self.change_road()  # Choose the first route

    def step(self):
        self.travel_time += 1

    # Returns the next route the vehicle should take.
    # Computes the shortest  
    # Params:
    #   node: route start node
    def next_route_dumb(self, node):
        try:
            path = nx.dijkstra_path(self.model.G, node, self.model.end, weight="free_flow_time")
            if node == self.model.end:
                return -1
            else:
                return self.model.G[node][path[1]]['agent']
        except nx.NetworkXNoPath:
            print(f"Vehicle Error: No path exists between {node.label} and {self.model.end.label}.")
            return -1
        except nx.NodeNotFound as e:
            print(f"Vehicle Error: {e}")
            return -1

    # !
    # \brief Updates vehicles 'position' in the route.
    # designed for the vehicle that knows the network
    # \param route The route the vehicle is in.
    def next_route_gps(self, node):
        try:
            path = nx.dijkstra_path(self.model.G, node, self.model.end, weight="travel_time")
            if node == self.model.end:
                return -1
            else:
                return self.model.G[node][path[1]]['agent']
        except nx.NetworkXNoPath:
            print(f"No path exists between {node} and {self.model.end.label}.")
            return -1
        except nx.NodeNotFound as e:
            print(f"Error: {e}")
            return -1

    # !
    # \brief Updates vehicles 'position' in the route.
    # \param route The route the vehicle is in.
    def change_road(self):
        if self.pos == 0:
            node = self.model.start
        else:
            node = self.pos.destination

        if self.prob_gps > 0:
            if random() < self.prob_gps:
                self.pos = self.next_route_gps(node)
            else:
                self.pos = self.next_route_dumb(node)
        else:
            self.pos = self.next_route_dumb(node)

        if self.pos != -1:
            self.pos.add_vehicle(self)

    # !
    # \brief Get the time the vehicle has been in the queue.
    @property
    def time_in_queue(self):
        return self._time_in_queue

    # !
    # \brief Returns a string representation of the vehicle.
    def __str__(self):
        return f"Vehicle: {self._route} {self.travel_time} {self._time_in_queue}"
