
#! 
# \file vehicle.py
# \brief A class representing a vehicle.
class Vehicle:

    #!
    # \brief Constructor for the Vehicle class.
    # \param route The route the vehicle is currently in.
    # \param travel_time The time it takes for the vehicle to travel the route.
    def __init__(self, travel_time : int, route = None): 

        self._time_in_queue : int = 0
        self._route = route
        self._travel_time : travel_time = travel_time


    #!
    # \brief Get the route of the vehicle.
    @property
    def route(self):
        return self._route
    

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
    # \brief Set the time the vehicle has been in the queue.
    @time_in_queue.setter
    def time_in_queue(self, time : int):
        self._time_in_queue = time

    
    #!
    # \brief Set the route of the vehicle.
    @route.setter
    def route(self, route):
        self._route = route

    
    #!
    # \brief Set the travel time of the vehicle.
    @travel_time.setter
    def travel_time(self, time : int):
        self._travel_time = time


    #!
    # \brief Moves the vehicle to a new route.
    # \param route The route to move to.
    def move(self, route):
        self._route = route
        self._time_in_queue = 0
        self._travel_time = route.bpr_function()

    
    #!
    # \brief Clears the vehicle's route.
    def clear_route(self):
        self._route = None
        self._time_in_queue = 0
        self._travel_time = 0


    #!
    # \brief Returns a string representation of the vehicle.
    def __str__(self):
        return f"Vehicle: {self._route} {self._travel_time} {self._time_in_queue}"
    
    
