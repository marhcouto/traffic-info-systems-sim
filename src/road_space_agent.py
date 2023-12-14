from mesa import Agent


#!
# \file road_space_agent.py
# \brief A class representing a spot on the road.
class RoadSpaceAgent(Agent):

    #!
    # \brief Constructor for the RoadSpaceAgent class.
    # \param unique_id The unique id of the agent.
    # \param model The model the agent belongs to.
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


    def step(self):
        # Do nothing
        pass