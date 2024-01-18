from mesa import Agent


# !
# \file network_node.py
# \brief A class representing a node in the network.
class NetworkNode(Agent):
    # !
    # \brief Constructor for the NetworkNode class.
    def __init__(self, unique_id, model, label):
        super().__init__(unique_id, model)
        self.label = label  # Label of the node

    def step(self):
        pass  # Do nothing
