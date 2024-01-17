from mesa import Agent, Model

from model.vehicle import Vehicle
from model.network_node import NetworkNode
from enum import Enum

class RouteState(Enum):
    FREE = 1
    FULL = 2
    CONGESTED = 3
    HIGHLY_CONGESTED = 4

#!
# \file car_agent.py
# \brief A class representing a vehicle.
class RouteAgent(Agent):

    #!
    # \brief Constructor for the CarAgent class.
    # \param unique_id The unique id of the agent.
    # \param models The models the agent belongs to.
    def __init__(self, unique_id : int, model : Model, capacity : int, 
                 free_flow_time: int, alpha : float = 0.15, beta : float = 4,
                 origin : NetworkNode = None, destination : NetworkNode = None):
        super().__init__(unique_id, model)
        self.capacity : int = capacity # in vehicles per minute
        self.free_flow_time : int = free_flow_time # in minutes
        self.alpha : float = alpha # parameter for the BPR function
        self.beta : float = beta # parameter for the BPR function
        self.origin = origin 
        self.destination : NetworkNode = destination
        self.state : str = RouteState.FREE
        self.queue : [Vehicle, float] = []# list of cars in the route
                                    # takes to travel the route at free flow
        
        self.tt_history = []
        self.it_history = []

    #!
    # \brief Updates vehicles 'position' in the route.
    def step(self):

        if self.model.gps_delay > 0:
            if len(self.tt_history) < self.model.gps_delay - 1:
                self.tt_history.append(self.travel_time())
                self.model.G[self.origin][self.destination]['travel_time'] = self.free_flow_time
            else:
                self.tt_history.append(self.travel_time())
                self.model.G[self.origin][self.destination]['travel_time'] = self.tt_history.pop(0)
        


        if len(self.queue) <= 0:
            return

        for line in self.queue:
            line[1] -= 1

        while len(self.queue) > 0 and self.queue[0][1] <= 0:
            vehicle = self.queue.pop(0)
            vehicle[0].change_road()


        if self.volume_to_capacity_ratio() > 1.5:
            self.state = RouteState.HIGHLY_CONGESTED
        elif self.volume_to_capacity_ratio() > 1.20:
            self.state = RouteState.CONGESTED
        elif self.volume_to_capacity_ratio() > 1:
            self.state = RouteState.FULL
        else:
            self.state = RouteState.FREE

    #!
    # \brief Adds a vehicle to the route.
    # \param vehicle The vehicle to add.
    def add_vehicle(self, vehicle):
        self.queue.append([vehicle, self.travel_time()])
        if self.model.gps_delay == 0:
            self.model.G[self.origin][self.destination]['travel_time'] = self.travel_time()

    #!
    # \brief Calculate the travel time for a vehicle entering the route.
    # \return The travel time for the vehicle.
    def travel_time(self):
        return self.free_flow_time * (1 + self.alpha * \
                                (self.volume() / self.capacity) ** self.beta)

    #!
    # \brief Returns the volume to capacity ratio of the route.
    # \return The volume to capacity ratio of the route.
    def volume_to_capacity_ratio(self):
        return self.volume() / self.capacity


    #!
    # \brief Returns the volume of the route.
    # \return The volume of the route.
    def volume(self):
        return len(self.queue)

