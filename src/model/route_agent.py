from enum import Enum

from mesa import Agent, Model

from model.network_node import NetworkNode
from model.vehicle import Vehicle


# RouteState Enum
class RouteState(Enum):
    FREE = 1
    FULL = 2
    CONGESTED = 3
    HIGHLY_CONGESTED = 4


# RouteAgent class
# Represents a route queue agent in the network
class RouteAgent(Agent):

    # Constructor for the RouteAgent class
    # Params:
    #   unique_id: unique id of the agent
    #   model: the model the agent is in
    #   capacity: the capacity of the route (vehicle / min)
    #   free_flow_time: the time it takes to travel the route at free flow (min)
    #   alpha: adjustable parameter for the BPR function
    #   beta: adjustable parameter for the BPR function
    #   origin: the origin node of the route
    #   destination: the destination node of the route
    def __init__(self, unique_id: int, model: Model, capacity: int,
                 free_flow_time: int, alpha: float = 0.15, beta: float = 4,
                 origin: NetworkNode = None, destination: NetworkNode = None):
        super().__init__(unique_id, model)
        self.capacity: int = capacity
        self.free_flow_time: int = free_flow_time
        self.alpha: float = alpha
        self.beta: float = beta
        self.origin = origin
        self.destination: NetworkNode = destination

        self.state: str = RouteState.FREE  # Initial state is set as FREE
        self.queue: [Vehicle, float] = []  # Queue of vehicles in the route
        self.tt_history = []  # History of travel times for the route (information delay)

    # Step function for the RouteAgent class
    def step(self):

        # Update travel time history
        

        if len(self.queue) <= 0:
            return

        for line in self.queue:
            line[1] -= 1

        # Remove vehicles that have reached their destination
        while len(self.queue) > 0 and self.queue[0][1] <= 0:
            vehicle = self.queue.pop(0)
            vehicle[0].change_road()

       

    # Add a vehicle to the route
    def add_vehicle(self, vehicle: Vehicle):

        # If there is delay then update travel time history
        self.update_history()
        print(self.travel_time(), round(self.travel_time()))
        self.queue.append([vehicle, round(self.travel_time())])
        self.update_state()

            
    # Update the travel time history in case there is delay
    def update_history(self):
        if self.model.gps_delay > 0:

            # If the history is not full then set the travel time to free flow time
            if len(self.tt_history) < self.model.gps_delay:
                self.model.G[self.origin][self.destination]['travel_time'] = self.free_flow_time
            else: # else set the travel time to the oldest travel time in the history
                self.model.G[self.origin][self.destination]['travel_time'] = self.tt_history.pop(0)
            
            self.tt_history.append(self.travel_time())
        else:
            self.model.G[self.origin][self.destination]['travel_time'] = self.travel_time()

    def update_state(self):
         # Update the state of the route
        if self.volume_to_capacity_ratio() >= 1.5:
            self.state = RouteState.HIGHLY_CONGESTED
        elif self.volume_to_capacity_ratio() >= 1.20:
            self.state = RouteState.CONGESTED
        elif self.volume_to_capacity_ratio() >= 1:
            self.state = RouteState.FULL
        else:
            self.state = RouteState.FREE

    # Calculate the travel time of the route with the BPR function
    def travel_time(self):
        return self.free_flow_time * (1 + self.alpha * \
                                      (self.volume() / self.capacity) ** self.beta)

    # Calculate the current volume to capacity ratio of the route
    def volume_to_capacity_ratio(self):
        return self.volume() / self.capacity

    # Get the current volume of the route
    def volume(self):
        return len(self.queue)
