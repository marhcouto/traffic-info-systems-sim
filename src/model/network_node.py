from mesa import Agent, Model

class NetworkNode(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass # Do nothing
