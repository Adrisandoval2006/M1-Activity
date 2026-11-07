
import mesa
import numpy as np
import pandas as pd

class RobotAgent(mesa.Agent):

    def __init__(self, model):
        super().__init__(model)
        self.movements = 0

    def step(self):
        current_pos = self.pos

        # Check if the current cell is dirty
        if current_pos in self.model.dirty_cells:
            self.model.dirty_cells.remove(current_pos)
            return

        # Get the 8 neighboring cells
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        # Select a random neighboring cell
        next_pos = self.model.random.choice(neighbors)

        # Move only if the destination is empty
        if self.model.grid.is_cell_empty(next_pos):
            self.model.grid.move_agent(self, next_pos)
            self.movements += 1
            self.model.total_moves += 1
