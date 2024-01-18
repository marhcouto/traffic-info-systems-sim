import networkx as nx
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from model.network_node import NetworkNode
from model.route_agent import RouteAgent
from model.vehicle import Vehicle


def function1(model, index):
    return model.routes[index].volume_to_capacity_ratio()


# !
# \file network_model.py
# \brief A class representing the road network models.
class NetworkModel(Model):

    # !
    # \brief Constructor for the NetworkModel class.
    def __init__(self, num_vehicles_s: int, start_node, end_node, nodes: list, roads: list, prob_gps: float, gps_delay,
                 alpha: float = 0.15, beta: float = 4):

        self.alpha: float = alpha  # parameter for the BPR function
        self.beta: float = beta  # parameter for the BPR function
        self.num_vehicles_s = num_vehicles_s  # Vehicles being generated at each moment
        self.prob_gps = prob_gps  # Probability of a vehicle following the GPS
        self.gps_delay = gps_delay  # Number of iterations the GPS is delayed
        self.current_id = -1  # current agent id
        self.schedule = RandomActivation(self)

        self.routes = []  # List of routes in the network
        self.create_graph(start_node, end_node, nodes, roads)
        self.active_vehicles = []  # Vehicles currently in the network
        self.total_travel_time = 0  # Total travel time of all vehicles
        self.num_killed_vehicles = 0  # Number of vehicles that reached their destination
        self.iterations = 0  # Number of iterations the model has run
        self.max_ratio_sum = 0  # Sum of the maximum volume to capacity ratio of any road
        self.best_time = NetworkModel.get_best_path(self.G, self.start, self.end, "free_flow_time")

        model_reporters_dictionary = {"Average Travel Time": self.avg_travel_time,
                                      "Average Travel Efficiency": NetworkModel.avg_travel_efficiency,
                                      "Max Congestion Ratio": self.avg_max_vc_ratio,
                                      "No. Vehicles Complete": lambda a: self.num_killed_vehicles}

        for i in range(len(self.routes)):
            model_reporters_dictionary[str(self.routes[i].origin.unique_id) + " -> " +
                                       str(self.routes[i].destination.unique_id)] = lambda a, i=i: function1(self, i)
        self.data_collector = DataCollector(model_reporters=model_reporters_dictionary)

    # !
    # \brief gets the best shortest path according to the weight parameter
    # \param graph Graph to be used
    # \param start Start node
    # \param end End node
    # \param weight String denoting the value to take as weight from the edges
    # \return ArrayLike
    def get_best_path(graph, start, end, weight: str):
        try:
            path = nx.dijkstra_path(graph, start, end, weight=weight)

            sum = 0
            for i in range(len(path) - 1):
                sum += graph[path[i]][path[i + 1]][weight]

            return sum
        except nx.NetworkXNoPath:
            print(f"No path exists between {start} and {end}.")
            return None
        except nx.NodeNotFound as e:
            print(f"Error: {e}")
            return None

    #
    # !
    # \brief Creates the roads of the network and schedules agents.
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

        print("done")
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

    # !
    # \brief Creates the vehicles of the network and schedules agents.
    def create_vehicles(self):
        for i in range(self.num_vehicles_s):
            v = Vehicle(self.next_id(), self, self.prob_gps)
            self.active_vehicles.append(v)
            self.schedule.add(v)

    # !
    # \brief Removes vehicles that have reached their destination.
    def kill_vehicles(self):
        vehicles = self.active_vehicles.copy()
        for vehicle in vehicles:
            if vehicle.pos == -1:
                self.schedule.remove(vehicle)
                self.num_killed_vehicles += 1
                self.total_travel_time += vehicle.travel_time
                self.active_vehicles.remove(vehicle)

    # !
    # \brief calculates the travel efficiency, which is the best time possible between the points
    # divided by the average time traveled per vehicle
    # \return average travel efficiency 
    def avg_travel_efficiency(model):
        return 0 if model.num_killed_vehicles == 0 else model.best_time \
                                                        / (model.total_travel_time / model.num_killed_vehicles)

    # !
    # \brief calculates the average travel time
    # \return average travel time
    def avg_travel_time(model):
        return 0 if model.num_killed_vehicles == 0 else model.total_travel_time \
                                                        / model.num_killed_vehicles

    def avg_max_vc_ratio(model):
        return 0 if model.iterations == 0 else model.max_ratio_sum / model.iterations

    # !
    # \brief calculates the maximum volume to capacity ratio of any road
    # which illustrates the maximum congestion values
    def update_max_vc_ratio(self):

        max_ratio = 0

        for route in self.routes:
            if route.volume_to_capacity_ratio() > max_ratio:
                max_ratio = route.volume_to_capacity_ratio()

        self.max_ratio_sum += max_ratio

    # !
    # \brief Executes the steps of the agents of the models.
    def step(self):
        self.data_collector.collect(self)
        self.create_vehicles()
        self.kill_vehicles()
        self.update_max_vc_ratio()
        self.schedule.step()
        self.iterations += 1
