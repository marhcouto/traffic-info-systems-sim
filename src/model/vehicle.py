from mesa import Agent, Model
from model.network_node import NetworkNode

#! 
# \file vehicle.py
# \brief A class representing a vehicle.
class Vehicle(Agent):

    #!
    # \brief Constructor for the Vehicle class.
    # \param route The route the vehicle is currently in.
    # \param travel_time The time it takes for the vehicle to travel the route.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self._travel_time = 0
        self.queue = 0
        self.pos = 0
        self.change_road()

    def step(self):
        self.travel_time += 1

    def decide_road(self, node):
        possible_routes = self.model.G.out_edges(node)

        max_idx = 0
        max_route = 0
        for u,v in possible_routes:
            route = self.model.G[u][v]['agent']
            if route.travel_time() > max_idx:
                max_idx = route.travel_time()
                max_route = route

        if max_route == 0:
            return -1
        else:
            return max_route

    def change_road(self):
        if self.pos == 0:
            route = self.decide_road(self.model.start)
        else:
            route = self.decide_road(self.pos.destination)

        self.pos = route
        if route != -1:
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
    
    
