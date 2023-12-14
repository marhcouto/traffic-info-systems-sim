from mesa import Agent

#!
# \file car_agent.py
# \brief A class representing a vehicle.
class CarAgent(Agent):

    #!
    # \brief Constructor for the CarAgent class.
    # \param unique_id The unique id of the agent.
    # \param model The model the agent belongs to.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.speed = 1

    #!
    # \brief Moves the agent.
    def step(self):
        self.model.grid.move_agent(self, (self.pos[0] + self.speed, self.pos[1] + self.speed))