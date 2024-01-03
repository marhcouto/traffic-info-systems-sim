from mesa import Agent, Model

class NetworkNode(Agent):
    
    def __init__(self, unique_id, model, label):
        super().__init__(unique_id, model)
        self.label = label

    def step(self):
        pass # Do nothing
