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


def network_portrayal(G):
    # The models ensures there is always 1 agent per node

    def node_color(node):
        if G.out_degree(node) == 0:
            return "#003399"
        elif G.in_degree(node) == 0:
            return "#99ccff"
        else:
            return "#999999"

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
    "prob_informed": 0.0,
    "tablet_delay": 0,
}

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
    "prob_informed": 0.0,
    "tablet_delay": 0,
}

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
    "prob_informed": 0.0,
    "tablet_delay": 0,
}

network = NetworkModule(network_portrayal, 500, 500)
chart1 = ChartModule([{"Label": "Average Travel Time", "Color": "Black"},
                    {"Label": "Average Travel Efficiency", "Color": "Green"}, 
                      {"Label": "Max Congestion Ratio", "Color": "Red"},
                      {"Label": "No. Vehicles Complete", "Color": "Blue"}],
                    data_collector_name='data_collector')
# chart2 = ChartModule([{"Label": "Average Travel Efficiency", "Color": "Black"}, 
#                       {"Label": "Max Congestion Ratio", "Color": "Red"}],
#                     data_collector_name='data_collector')

series = [{"Label": str(road[0]) + " -> " + str(road[1]), "Color": "Black"} for road in scenarios.large_model.roads()]
barchart = BarChartModule(series, canvas_width=100*len(series), data_collector_name='data_collector')

server : ModularServer = ModularServer(NetworkModel, [network, barchart, chart1],
                                    "Network Model", smart)
server.port : int = 8527 # The default
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