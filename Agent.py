"""
Reactive cleaning robot agent.
Authors: Adriana Sandoval Santos - A01667445
         Marbella Barba De los Santos - A01660946
         Javier Padilla Marcial - A01660945
         Camila Quintanilla Cabrera - A01662397
         Alani Daniel Garcia Maya - A01277308
Date: 2026-11-06
"""

import mesa

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),            (0, 1),
    (1, -1),  (1, 0),   (1, 1)
]

class RobotAgent(mesa.Agent):
    # Initializes the robot's individual counters.
    # Parameters: model: Simulation model containing this robot.
    # Returns: None.
    def __init__(self, model):
        super().__init__(model)
        self.movements = 0
        self.cellsCleaned = 0
        self.actions = 0

    # Cleans the current cell or attempts one random movement.
    # Parameters: None.
    # Returns: None.
    def step(self):
        self.actions += 1
        currentPos = self.pos

        if currentPos in self.model.dirtyCells:
            self.model.dirtyCells.remove(currentPos)
            self.cellsCleaned += 1
        else:
            dx, dy = self.random.choice(DIRECTIONS)
            nextPos = (currentPos[0] + dx, currentPos[1] + dy)

            if not self.model.grid.out_of_bounds(nextPos):
                self.model.grid.move_agent(self, nextPos)
                self.movements += 1
                self.model.totalMoves += 1