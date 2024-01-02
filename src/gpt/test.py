from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule
from network_model import NetworkModel

def network_portrayal(G):
    # The portrayal is a dictionary with network info.
    portrayal = dict()
    portrayal['nodes'] = [{'id': agent.unique_id, 'size': 3} for agent in G.nodes()]
    portrayal['edges'] = [{'source': source.unique_id, 'target': target.unique_id, "color": "#e8e8e8"} for source, target in G.edges()]
    return portrayal

# Create a network visualization module
network = NetworkModule(network_portrayal, 500, 500)

# Create a Mesa server
server = ModularServer(NetworkModel,
                       [network],
                       "Network Model",
                       {"N": 3})


server.launch()
