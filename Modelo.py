import mesa
from mesa.space import MultiGrid
from Agentes import RobotAgent
 
 
class CleaningModel(mesa.Model):
    """Cuarto de width x height con robots de limpieza reactivos."""
 
    def __init__(self, dirty_per, max_t, num_agents=7, width=10, height=10,
                 rng=None):
        super().__init__(rng=rng)
        if not 0 <= dirty_per <= 100:
            raise ValueError("dirty_per debe estar entre 0 y 100")
 
        self.dirty_per = dirty_per
        self.max_t = max_t
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.total_moves = 0
        self.completion_time = None
        self.current_step = 0
 
        self.grid = MultiGrid(width, height, torus=False)
 
        total_cells = width * height
        num_dirty_cells = int(total_cells * dirty_per / 100)
        all_cells = [(x, y) for x in range(width) for y in range(height)]
        self.dirty_cells = set(self.random.sample(all_cells, num_dirty_cells))
 
        RobotAgent.create_agents(model=self, n=num_agents)
        for agent in self.agents:
            self.grid.place_agent(agent, (0, 0))
 
        if not self.dirty_cells:
            self.completion_time = 0
            self.running = False
 
    def step(self):
        if not self.running:
            return
 
        self.agents.shuffle_do("step")
        self.current_step += 1
 
        if not self.dirty_cells:
            self.completion_time = self.current_step
            self.running = False
        elif self.current_step >= self.max_t:
            self.running = False
 
    def clean_percentage(self):
        total_cells = self.width * self.height
        return (total_cells - len(self.dirty_cells)) / total_cells * 100
 
    def get_stats(self):
        if self.completion_time is not None:
            exec_time = self.completion_time
        else:
            exec_time = self.current_step
 
        return {
            "execution_time": exec_time,
            "cleaned_percentage": self.clean_percentage(),
            "remaining_dirty_cells": len(self.dirty_cells),
            "total_moves": self.total_moves,
            "all_clean": self.completion_time is not None,
        }