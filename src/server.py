from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa import Agent

from network_model import NetworkModel
from road_space_agent import RoadSpaceAgent
from car_agent import CarAgent

#!
# \file server.py
# \brief Function that defines the visual
#of the agents.
# \param agent The agent to be portrayed.
# \return The portrayal of the agent (dict).
def agent_portrayal(agent : Agent):
    if type(agent) == RoadSpaceAgent:
        portrayal : dict = {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "gray", "w": 1, "h": 1}
    elif type(agent) == CarAgent:
        portrayal : dict = {"Shape": "circle", "Filled": "true", "Layer": 1, "Color": "blue", "r": 0.5}
    else:
        portrayal : dict = {"Shape": "circle", "Filled": "true", "Layer": 1, "Color": "red", "r": 0.5}
    return portrayal


grid : CanvasGrid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
server : ModularServer = ModularServer(NetworkModel, [grid], "Network Model", {"N":10, "width": 100, "height": 100})
server.port : int = 8521 # The default
server.launch()