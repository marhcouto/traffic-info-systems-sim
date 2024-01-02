from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule, ChartModule
from mesa import Agent
import networkx as nx
from model.network_model import NetworkModel

def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(node):
        return "#FF00000"

    def edge_color(node1, node2):
        return '#e8e8e8'

    def edge_width(node1, node2):
        return G.get_edge_data(node1, node2)['capacity'] / 5

    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(node),
                           'tooltip': "Node",
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


model_params = {}
network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([{"Label": "Queue Length", "Color": "Black"}],
                    data_collector_name='data_collector')


server : ModularServer = ModularServer(NetworkModel, [network, chart], 
                                       "Network Model", model_params)
server.port : int = 8527 # The default
server.launch()