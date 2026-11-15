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

    # Initializes the robot and its movement counter.
    # Parameters:
    # uniqueId: Unique identifier of the robot.
    # model: Model containing the robot.
    # Returns: None.
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.movements = 0

    # Cleans the current cell or attempts a random movement.
    # Parameters: None.
    # Returns: None.
    def step(self):
        currentPos = self.pos

        if currentPos in self.model.dirtyCells:
            self.model.dirtyCells.remove(currentPos)
        else:
            dx, dy = self.random.choice(DIRECTIONS)
            nextPos = (currentPos[0] + dx, currentPos[1] + dy)

            if not self.model.grid.out_of_bounds(nextPos):
                self.model.grid.move_agent(self, nextPos)
                self.movements += 1
                self.model.totalMoves += 1
