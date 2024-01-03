from mesa import Agent, Model

from model.vehicle import Vehicle
from model.network_node import NetworkNode


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
        self.capacity : int = capacity # number of cars that can be in route
        self.free_flow_time : int = free_flow_time # time it
        self.alpha : float = alpha # parameter for the BPR function
        self.beta : float = beta # parameter for the BPR function
        self.origin = origin
        self.destination : NetworkNode = destination

        self.queue : [Vehicle, float] = []# list of cars in the route
                                    # takes to travel the route at free flow

        



    #!
    # \brief Updates vehicles 'position' in the route.
    def step(self):

        if len(self.queue) <= 0:
            return

        for line in self.queue:
            line[1] -= 1

        while self.queue[0][1] <= 0:
            vehicle = self.queue.pop(0)
            vehicle[0].change_road()

            # self.destination.add_vehicle()
            # Put vehicle to the next route if it exists

    #!
    # \brief Adds a vehicle to the route.
    # \param vehicle The vehicle to add.
    def add_vehicle(self, vehicle):
        self.queue.append([vehicle, self.travel_time()])

    #!
    # \brief Calculate the travel time for a vehicle entering the route.
    # \return The travel time for the vehicle.
    def travel_time(self):
        return self.free_flow_time * (1 + self.alpha * \
                                (self.volume() / self.capacity) ** self.beta)


    def flow_to_capacity_ratio(self):
        return self.volume() / self.capacity


    #!
    # \brief Returns the volume of the route.
    def volume(self):
        return len(self.queue)

