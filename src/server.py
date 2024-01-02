from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule, ChartModule
from mesa import Agent
import networkx as nx
from model.road import Road
from model.node import Node
from model.network_model import NetworkModel
from road_space_agent import RoadSpaceAgent
from car_agent import CarAgent

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
                           'color': "#e8e8e8",
                           'tooltip': "Node",
                           'id': node.id,
                           }
                          for node in G.nodes]

    portrayal['edges'] = [{'source': source.id,
                           'target': target.id,
                           'color': "#FF0000",
                           'width': edge_width(source, target),
                           }
                          for (source, target) in G.edges]

    return portrayal

nodeA = Node("A")
nodeB = Node("B")
nodeC = Node("C")

roads = []
road1 = Road(nodeA, nodeB, 40)
road2 = Road(nodeA, nodeC, 35)
road3 = Road(nodeB, nodeC, 50)

roads.append(road1)
roads.append(road2)
roads.append(road3)

model_params = {'N': 10, 'roads': roads}




network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([{'Label': 'Highly Congested', 'Color': '#FF0000'},
                     {'Label': 'Congested', 'Color': '#008000'},
                     {'Label': 'Regular', 'Color': '#00C5CD'},
                     ])


server : ModularServer = ModularServer(NetworkModel, [network], "Network Model", model_params)
server.port : int = 8524 # The default
server.launch()


#nx.draw(NetworkModel)

#def show_graph(NetworkModel):