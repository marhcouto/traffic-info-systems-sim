from mesa import Agent, Model

from vehicle import Vehicle

#!
# \file car_agent.py
# \brief A class representing a vehicle.
class RouteAgent(Agent):

    #!
    # \brief Constructor for the CarAgent class.
    # \param unique_id The unique id of the agent.
    # \param model The model the agent belongs to.
    def __init__(self, unique_id : int, model : Model, capacity : int, 
                 avg_speed : int, distance : int, alpha : float = 0.15, beta : float = 4):
        super().__init__(unique_id, model)

        self.avg_speed : int = avg_speed # km/h, same as max legal speed
        self.distance : int = distance # kms
        self.queue : int = [] # list of cars in the route
        self.capacity : int = capacity # number of cars that can be in route
        self.free_flow_time : int = self.distance / self.avg_speed # time it
                                    # takes to travel the route at free flow
        self.alpha : float = alpha # parameter for the BPR function
        self.beta : float = beta # parameter for the BPR function

    #!
    # \brief Updates vehicles 'position' in the route.
    def step(self):

        for vehicle in self.queue:
            vehicle.time_in_queue += 1

        if len(self.queue) <= 0:
            return
        
        while True:
            vehicle : Vehicle = self.queue[0]

            if vehicle.time_in_queue >= vehicle.travel_time:
                self.queue.pop(0)
                vehicle.clear_route()
                # Put vehicle to the next route if it exists
            else:
                break

    
    #!
    # \brief Adds and creates vehicles to the route.
    def add_new_vehicle(self):
        vehicle = Vehicle(self.bpr_function(), self)
        self.queue.append(vehicle)

    #!
    # \brief Adds a vehicle to the route.
    # \param vehicle The vehicle to add.
    def add_vehicle(self, vehicle : Vehicle):
        vehicle.travel_time = self.bpr_function()
        self.queue.append(vehicle)


    #!
    # \brief Calculate the travel time for a vehicle entering the route.
    # \return The travel time for the vehicle.
    def bpr_function(self):
        return self.free_flow_time * (1 + 0.15 * \
                                (self.volume() / self.capacity) ** 4)


    #!
    # \brief Returns the volume of the route.
    def volume(self):
        return len(self.queue)
    