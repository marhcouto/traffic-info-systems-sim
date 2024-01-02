from mesa import Agent, Model

class NetworkNode(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self._ingoing_routes = []
        self._outgoing_routes = []
        # TODO: complete this

    def step(self):
        pass # Do nothing