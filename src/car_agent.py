from mesa import Agent


class CarAgent(Agent):
    """An agent that represents a vehicle."""

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's attribute and set the initial values.
        self.speed = 1

    def step(self):
        # Move the agent
        print("I am moving!")
        self.model.grid.move_agent(self, (self.pos[0] + self.speed, self.pos[1] + self.speed))