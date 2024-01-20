import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation, BaseScheduler

from model.network_node import NetworkNode
from model.route_agent import RouteAgent
from model.vehicle import Vehicle


def function1(model, index):
    return model.routes[index].volume_to_capacity_ratio()



# NetworkModel class
# Represents  a network model
class NetworkModel(Model):

    # Constructor for the Network class
    # Params:
    #   num_vehicle_s: number of vehicles to be generated at each step
    #   start_node: the start node of the network
    #   end_node: the end node of the network
    #   nodes: list of nodes in the network
    #   roads: list of roads in the network
    #   prob_gps: probability of a vehicle following the GPS
    #   gps_delay: number of iterations the GPS is delayed
    #   alpha: parameter for the BPR function
    #   beta: parameter for the BPR function
    def __init__(self, num_vehicles_s: int, start_node, end_node, nodes: list, roads: list, prob_gps: float, gps_delay,
                 alpha: float = 0.15, beta: float = 4):

        self.alpha: float = alpha
        self.beta: float = beta
        self.num_vehicles_s = num_vehicles_s
        self.prob_gps = prob_gps
        self.gps_delay = gps_delay
        self.current_id = -1
        self.schedule = BaseScheduler(self) # Create the scheduler that will run the model

        self.routes = []  # List of routes in the network
        self.create_graph(start_node, end_node, nodes, roads)
        self.active_vehicles = []  # Vehicles currently in the network
        self.total_travel_time = 0  # Total travel time of all vehicles
        self.num_killed_vehicles = 0  # Number of vehicles that reached their destination
        self.iterations = 0  # Number of iterations the model has run
        self.max_ratio_sum = 0  # Sum of the maximum volume to capacity ratio of any road
        self.best_time = self.get_best_time()

        model_reporters_dictionary = {"Average Travel Time": self.avg_travel_time,
                                      "Average Travel Efficiency": NetworkModel.avg_travel_efficiency,
                                      "Max Congestion Ratio": self.avg_max_vc_ratio,
                                      "No. Vehicles Complete": lambda a: self.num_killed_vehicles}

        for i in range(len(self.routes)):
            model_reporters_dictionary[str(self.routes[i].origin.unique_id) + " -> " +
                                       str(self.routes[i].destination.unique_id)] = lambda a, i=i: function1(self, i)
        self.data_collector = DataCollector(model_reporters=model_reporters_dictionary)

    # Get the best time possible between the start and end nodes 
    def get_best_time(self):
        try:
            path = nx.dijkstra_path(self.G, self.start, self.end, weight="free_flow_time")

            sum = 0
            for i in range(len(path) - 1):
                sum += self.G[path[i]][path[i + 1]]["free_flow_time"]

            return sum
        except nx.NetworkXNoPath:
            print(f"No path exists between {self.start} and {self.end}.")
            return None
        except nx.NodeNotFound as e:
            print(f"Error: {e}")
            return None

    # Create the roads of the network and schedules agents.
    # Params:
    #   start_node: the start node of the network
    #   end_node: the end node of the network
    #   nodes: list of nodes in the network
    #   roads: list of roads in the network
    def create_graph(self, start_node, end_node, nodes, roads):
        self.G = nx.DiGraph()
        node_dict = {}
        for node in nodes:
            n = NetworkNode(self.next_id(), self, node)
            self.schedule.add(n)
            self.G.add_node(n)
            if node == start_node:
                self.start = n
            elif node == end_node:
                self.end = n
            node_dict[node] = n

        for road in roads:
            if len(road) == 4:
                origin = road[0]
                destination = road[1]
                capacity = road[2]
                free_flow_time = road[3]

                route = RouteAgent(self.next_id(), self, capacity, free_flow_time, self.alpha, self.beta,
                                   node_dict[origin], node_dict[destination])

                self.G.add_edge(node_dict[origin], node_dict[destination], agent=route,
                                free_flow_time=route.free_flow_time, travel_time=route.free_flow_time,
                                informed_time=route.free_flow_time)
                self.routes.append(route)
                self.schedule.add(route)

    # Create the vehicles of the network and schedules agents.
    def create_vehicles(self):
        for i in range(self.num_vehicles_s):
            v = Vehicle(self.next_id(), self, self.prob_gps)
            self.active_vehicles.append(v)
            self.schedule.add(v)

    # Remove vehicles that have reached their destination.
    def kill_vehicles(self):
        vehicles = self.active_vehicles.copy()
        for vehicle in vehicles:
            if vehicle.pos == -1:
                self.schedule.remove(vehicle)
                self.num_killed_vehicles += 1
                self.total_travel_time += vehicle.travel_time
                self.active_vehicles.remove(vehicle)

    # Get the average travel efficiency of the network
    # Params:
    #   model: the model to get the average travel efficiency of
    def avg_travel_efficiency(model):
        return 0 if model.num_killed_vehicles == 0 else model.best_time \
                                                        / (model.total_travel_time / model.num_killed_vehicles)

    # Get the average travel time of the network
    # Params:
    #   model: the model to get the average travel time of
    def avg_travel_time(model):
        return 0 if model.num_killed_vehicles == 0 else model.total_travel_time \
                                                        / model.num_killed_vehicles

    # Get the average maximum volume to capacity ratio of any road
    # Params:
    #   model: the model to get the average maximum volume to capacity ratio of any road of
    def avg_max_vc_ratio(model):
        return 0 if model.iterations == 0 else model.max_ratio_sum / model.iterations

    # Update the maximum volume to capacity ratio of any road
    def update_max_vc_ratio(self):

        max_ratio = 0

        for route in self.routes:
            if route.volume_to_capacity_ratio() > max_ratio:
                max_ratio = route.volume_to_capacity_ratio()

        self.max_ratio_sum += max_ratio

    # Execute the steps of the agents of the models.
    def step(self):
        self.data_collector.collect(self)
        self.create_vehicles()
        self.kill_vehicles()
        self.update_max_vc_ratio()
        self.schedule.step()
        self.iterations += 1
