
import mesa
from mesa.space import MultiGrid

class CleaningModel(mesa.Model):

    def __init__(
        self,
        dirty_per,
        max_t,
        num_agentes=7,
        width=10,
        height=10,
        rng=None
    ):
        super().__init__(rng=rng)

        self.dirty_per = dirty_per
        self.max_t = max_t
        self.num_agentes = num_agentes
        self.width = width
        self.height = height

        self.total_moves = 0
        self.completion_time = None
        self.start_step = 0

        self.grid = MultiGrid(width, height, torus=False)

        total_cells = width * height
        self.num_dirty_cells = int(
            total_cells * dirty_per / 100
        )

        all_cells = [
            (x, y)
            for x in range(width)
            for y in range(height)
        ]

        dirty_pos = self.random.sample(
            all_cells,
            self.num_dirty_cells
        )

        self.dirty_cells = set(dirty_pos)

        if not self.dirty_cells:
            self.completion_time = 0

        # Import and create the robot agents
        from Agentes import RobotAgent

        RobotAgent.create_agents(
            model=self,
            n=self.num_agentes
        )

        # Place all robots at the initial position
        for agent in self.agents:
            self.grid.place_agent(agent, (0, 0))

    def step(self):

        if self.start_step >= self.max_t:
            return

        if not self.dirty_cells:
            return

        self.agents.shuffle_do("step")

        self.start_step += 1

        if not self.dirty_cells:
            self.completion_time = self.start_step
            print(
                f"All cells were cleaned in "
                f"{self.completion_time} steps."
            )

    def get_stats(self):

        total_cells = self.width * self.height
        cleaned_cells = total_cells - len(self.dirty_cells)

        self.clean_per = (
            cleaned_cells / total_cells
        ) * 100

        if self.completion_time is not None:
            exec_time = self.completion_time
        else:
            exec_time = self.start_step

        return {
            "execution_time": exec_time,
            "cleaned_percentage": self.clean_per,
            "remaining_dirty_cells": len(self.dirty_cells),
            "total_moves": self.total_moves
        }
