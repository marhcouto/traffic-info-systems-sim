from mesa import Agent


# NetworkNode class
# Represents a node agent in the network
class NetworkNode(Agent):

    # Constructor for the NetworkNode class
    # Params:
    #   unique_id: unique id of the network node
    #   model: the model the node is in
    #   label: the label of the node
    def __init__(self, unique_id, model, label):
        super().__init__(unique_id, model)
        self.label = label

    def step(self):
        pass  # Do nothing
