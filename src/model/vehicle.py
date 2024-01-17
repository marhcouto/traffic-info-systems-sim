from mesa import Agent, Model
from model.network_node import NetworkNode
from enum import Enum
import networkx as nx
from random import random

class VechicleType(Enum):
    FASTER = 1
    INFORMED = 2


#! 
# \file vehicle.py
# \brief A class representing a vehicle.
class Vehicle(Agent):

    #!
    # \brief Constructor for the Vehicle class.
    def __init__(self, unique_id, model, prob_gps):
        super().__init__(unique_id, model)
        self._travel_time = 0 # Time the vehicle has been traveling
        self.queue = 0 # Time the vehicle has been in the queue
        self.pos = 0 # Current position of the vehicle
        self.prob_gps = prob_gps # Probability of the vehicle following the GPS
        self.change_road()

    def step(self):
        self.travel_time += 1


    #!
    # \brief Updates vehicles 'position' in the route.
    # \param route The route the vehicle is in.
    def decide_road(self, node):

        possible_routes = self.model.G.out_edges(node)
        
        min_time = 99999999999999999999999
        min_route = 0
        for u, v in possible_routes:
            route = self.model.G[u][v]['agent']

            if route.travel_time() < min_time:
                min_time = route.travel_time()
                min_route = route

        if min_route == 0:
            return -1
        else:
            return min_route
        
    
    #!
    # \brief Updates vehicles 'position' in the route.
    # designed for the dumb vehicle that does not know the network
    # \param route The route the vehicle is in.
    def next_route_dumb(self, node):
        try:
            path = nx.dijkstra_path(self.model.G, node, self.model.end, weight="free_flow_time")
            if node == self.model.end:
                return -1
            else:
                return self.model.G[node][path[1]]['agent']
        except nx.NetworkXNoPath:
            print(f"Vehicle Error: No path exists between {node} and {self.model.end.label}.")
            return -1
        except nx.NodeNotFound as e:
            print(f"Vehicle Error: {e}")
            return -1

    #!
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

    #!
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


    #!
    # \brief Get the travel time of the vehicle.
    @property
    def travel_time(self):
        return self._travel_time
    

    #!
    # \brief Get the time the vehicle has been in the queue.
    @property
    def time_in_queue(self):
        return self._time_in_queue

    #!
    # \brief Set the travel time of the vehicle.
    @travel_time.setter
    def travel_time(self, time : int):
        self._travel_time = time

    #!
    # \brief Returns a string representation of the vehicle.
    def __str__(self):
        return f"Vehicle: {self._route} {self._travel_time} {self._time_in_queue}"
    
    
