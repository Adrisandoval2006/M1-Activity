import mesa
 
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]
 
class RobotAgent(mesa.Agent):
    """Robot reactivo: limpia si su celda esta sucia, si no, se mueve al azar."""
 
    def __init__(self, model):
        super().__init__(model)
        self.movements = 0
 
    def step(self):
        current_pos = self.pos
 
        if current_pos in self.model.dirty_cells:
            self.model.dirty_cells.remove(current_pos)
            return
 
        dx, dy = self.random.choice(DIRECTIONS)
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)
 
        if not self.model.grid.out_of_bounds(next_pos):
            self.model.grid.move_agent(self, next_pos)
            self.movements += 1
            self.model.total_moves += 1
