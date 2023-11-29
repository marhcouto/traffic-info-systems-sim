from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from car_agent import CarAgent

class NetworkModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.running = True

        # Create scheduler and assign it to the model
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = CarAgent(i, self)
            # Add the agent to the scheduler
            self.schedule.add(a)
            self.grid.place_agent(a, (i, i))


    def step(self):
        """Advance the model by one step."""

        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()