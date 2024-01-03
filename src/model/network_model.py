from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

import networkx as nx

from model.network_node import NetworkNode
from model.route_agent import RouteAgent
from model.vehicle import Vehicle




#!
# \file network_model.py
# \brief A class representing the road network models.
class NetworkModel(Model):

    #!
    # \brief Constructor for the NetworkModel class.
    # def __init__(self, nodes, roads, start, end):
    def __init__(self, num_vehicles_s: int, start_node, end_node, nodes: list, roads : list, alpha : float = 0.15, beta : float = 4, ):
        # self.running = True

        self.alpha : float = alpha # parameter for the BPR function
        self.beta : float = beta # param
        self.current_id = -1
        self.num_vehicles_s = num_vehicles_s
        self.schedule = RandomActivation(self)


        self.routes = []
        self.active_vehicles = []

        self.create_graph(start_node, end_node, nodes, roads)
        self.total_travel_time = 0
        self.num_killed_vehicles = 0

        self.data_collector = DataCollector(
            model_reporters={"Average Travel Time": avg_travel_time},

        )

    def find_shortest_path(self, node):
        try:
            path = nx.dijkstra_path(self.G, node, self.end, weight="agent.travel_time()")
            return path[1]
        except nx.NetworkXNoPath:
            print(f"No path exists between {node} and {self.end.label}.")
            return None
        except nx.NodeNotFound as e:
            print(f"Error: {e}")
            return None

    #!
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

        for road in roads:
            if len(road) == 4:
                origin = road[0]
                destination = road[1]
                capacity = road[2]
                free_flow_time = road[3]

                route = RouteAgent(self.next_id(), self, capacity, free_flow_time, self.alpha, self.beta, node_dict[origin], node_dict[destination])

                self.G.add_edge(node_dict[origin], node_dict[destination], agent = route)
                self.routes.append(route)
                self.schedule.add(route)

    def create_vehicles(self):
        for i in range(self.num_vehicles_s):
            v = Vehicle(self.next_id(), self)
            self.active_vehicles.append(v)
            self.schedule.add(v)

    def kill_vehicles(self):
        vehicles = self.active_vehicles.copy()
        for vehicle in vehicles:
            if vehicle.pos == -1:
                self.schedule.remove(vehicle)
                self.num_killed_vehicles += 1
                self.total_travel_time += vehicle.travel_time
                self.active_vehicles.remove(vehicle)

    def avg_travel_time(self):
        if self.num_killed_vehicles == 0:
            return 0
        else:
            return self.total_travel_time / self.num_killed_vehicles

    def max_volume_to_capacity_ratio(self):
        max_ratio = 0

        for route in self.routes:
            if route.volume_to_capacity_ratio() > max_ratio:
                max_ratio = route.volume_to_capacity_ratio()

        return max_ratio
    #!
    # \brief Executes the steps of the agents of the models.
    def step(self):
        self.create_vehicles()
        self.kill_vehicles()
        print(self.start.label)
        print(self.find_shortest_path(self.start).label)
        self.data_collector.collect(self)
        self.schedule.step()
        print(self.avg_travel_time())
        print(self.max_volume_to_capacity_ratio())

