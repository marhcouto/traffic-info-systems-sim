from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule, ChartModule, BarChartModule
from model.network_model import NetworkModel
from model.route_agent import RouteState
from mesa import batch_run
import scenarios.simple_model
import scenarios.long_option
import scenarios.small_model
import scenarios.large_model
import scenarios.medium_model

#!
# \file server.py
# \brief A class representing the server for the model.
def network_portrayal(G):
    # The models ensures there is always 1 agent per node

    #!
    # \brief Returns the color of a node.
    # \param node The node to get the color of.
    # \return The color of the node.
    def node_color(node):
        if G.out_degree(node) == 0:
            return "#003399"
        elif G.in_degree(node) == 0:
            return "#99ccff"
        else:
            return "#999999"

    #!
    # \brief Returns the color of an edge.
    # \param node1 The first node of the edge.
    # \param node2 The second node of the edge.
    # \return The color of the edge.
    def edge_color(node1, node2):
        if G.get_edge_data(node1, node2)['agent'].state == RouteState.FREE:
            return "#23b800"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.FULL:
            return "#ffd100"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.CONGESTED:
            return "#ff9900"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.HIGHLY_CONGESTED:
            return "#dc0d0d"
        else:
            print(G[node1][node2]['agent'].state)
            return '#e8e8e8'

    #!
    # \brief Returns the width of an edge.
    # \param node1 The first node of the edge.
    # \param node2 The second node of the edge.
    # \return The width of the edge.
    def edge_width(node1, node2):
        return G.get_edge_data(node1, node2)['agent'].capacity / 100

    portrayal = dict()
    portrayal['nodes'] = [{'size': 2,
                           'color': node_color(node),
                           'tooltip': node.label,
                           'id': node.unique_id,
                           }
                          for node in G.nodes()]

    portrayal['edges'] = [{'source': source.unique_id,
                           'target': target.unique_id,
                           'color': edge_color(source, target),
                           'width': edge_width(source, target),
                           }
                          for (source, target) in G.edges()]

    return portrayal

#!
# \brief Dictionary of parameters for the dumb agent (no GPS) to be used in the simulation.
dumb = {
    "num_vehicles_s": 30,
    "alpha": 0.15,
    "beta": 4,
    "nodes": scenarios.large_model.nodes(),
    "roads": scenarios.large_model.roads(),
    "start_node": scenarios.large_model.start_node(),
    "end_node": scenarios.large_model.end_node(),
    "prob_gps": 0.0,
    "gps_delay": 0,
}

#!
# \brief Dictionary of parameters for the half smart agent (50% change of following GPS) to be used in the simulation.
half_smart = {
    "num_vehicles_s": 30,
    "alpha": 0.15,
    "beta": 4,
    "nodes": scenarios.large_model.nodes(),
    "roads": scenarios.large_model.roads(),
    "start_node": scenarios.large_model.start_node(),
    "end_node": scenarios.large_model.end_node(),
    "prob_gps": 0.5,
    "gps_delay": 0,
}

#!
# \brief Dictionary of parameters for the smart agent (always follows GPS) to be used in the simulation.
smart = {
    "num_vehicles_s": 30,
    "alpha": 0.15,
    "beta": 4,
    "nodes": scenarios.large_model.nodes(),
    "roads": scenarios.large_model.roads(),
    "start_node": scenarios.large_model.start_node(),
    "end_node": scenarios.large_model.end_node(),
    "prob_gps": 1.0,
    "gps_delay": 0,
}

#!
# \brief Creates the server and launches it.
network = NetworkModule(network_portrayal, 500, 500)
chart1 = ChartModule([{"Label": "Average Travel Time", "Color": "Black"},
                    {"Label": "Average Travel Efficiency", "Color": "Green"}, 
                      {"Label": "Max Congestion Ratio", "Color": "Red"},
                      {"Label": "No. Vehicles Complete", "Color": "Blue"}],
                    data_collector_name='data_collector')

series = [{"Label": str(road[0]) + " -> " + str(road[1]), "Color": "Black"} for road in scenarios.large_model.roads()]
barchart = BarChartModule(series, canvas_width=100*len(series), data_collector_name='data_collector')

server : ModularServer = ModularServer(NetworkModel, [network, barchart, chart1],
                                    "Network Model", smart)
server.port : int = 8538 
server.launch()

model = NetworkModel(**dumb)
iterations = 500

for i in range(iterations):
    model.step()

print()
print("DUMB:")
print(model.avg_travel_time())
print(model.avg_max_vc_ratio())

model = NetworkModel(**half_smart)
iterations = 500

for i in range(iterations):
    model.step()

print()
print("HALF SMART:")
print(model.avg_travel_time())
print(model.avg_max_vc_ratio())

model = NetworkModel(**smart)
iterations = 500

for i in range(iterations):
    model.step()

print()
print("SMART:")
print(model.avg_travel_time())
print(model.avg_max_vc_ratio())