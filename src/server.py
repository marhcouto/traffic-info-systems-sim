from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from network_model import NetworkModel

def agent_portrayal(agent): 
    portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0, "Color": "red", "r": 0.5}
    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(NetworkModel, [grid], "Network Model", {"N":10, "width": 100, "height": 100})
server.port = 8521 # The default
server.launch()