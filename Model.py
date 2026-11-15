"""
Simulation model for reactive cleaning robots.
Authors: Adriana Sandoval Santos - A01667445
         Marbella Barba De los Santos - A01660946
         Javier Padilla Marcial - A01660945
         Camila Quintanilla Cabrera - A01662397
         Alani Daniel Garcia Maya - A01277308
Date: 2026-11-06
"""

import mesa
from mesa.space import MultiGrid
from Agent import RobotAgent

class CleaningModel(mesa.Model):

    # Initializes the room, dirty cells, and robots.
    # Parameters:
    # dirtyPercentage: Initial percentage of dirty cells.
    # maxSteps: Maximum number of simulation steps.
    # numAgents: Number of cleaning robots.
    # width: Number of room columns.
    # height: Number of room rows.
    # seed: Random seed for reproducibility.
    # Returns: None.
    def __init__(self, dirtyPercentage, maxSteps, numAgents=7,
                 width=10, height=10, seed=None):

        super().__init__(seed=seed)

        if not 0 <= dirtyPercentage <= 100:
            raise ValueError(
                "Dirty percentage must be between 0 and 100"
            )

        if width <= 0 or height <= 0:
            raise ValueError(
                "Room dimensions must be positive"
            )

        if numAgents <= 0:
            raise ValueError(
                "Number of agents must be positive"
            )

        if maxSteps < 0:
            raise ValueError(
                "Maximum steps cannot be negative"
            )

        self.dirtyPercentage = dirtyPercentage
        self.maxSteps = maxSteps
        self.numAgents = numAgents
        self.width = width
        self.height = height
        self.totalMoves = 0
        self.completionTime = None
        self.currentStep = 0

        self.grid = MultiGrid(width, height, torus=False)

        totalCells = width * height
        numDirtyCells = int(totalCells * dirtyPercentage / 100)

        allCells = [
            (x, y)
            for x in range(width)
            for y in range(height)
        ]

        self.dirtyCells = set(
            self.random.sample(allCells, numDirtyCells)
        )

        for i in range(numAgents):
            agent = RobotAgent(self)
            self.grid.place_agent(agent, (0, 0))

        if not self.dirtyCells:
            self.completionTime = 0
            self.running = False

        if maxSteps == 0:
            self.running = False

    # Executes one simulation step for all robots.
    # Parameters: None.
    # Returns: None.
    def step(self):

        if self.running:
            self.agents.shuffle_do("step")
            self.currentStep += 1

            if not self.dirtyCells:
                self.completionTime = self.currentStep
                self.running = False

            elif self.currentStep >= self.maxSteps:
                self.running = False

    # Calculates the percentage of clean cells.
    # Parameters: None.
    # Returns: Percentage of clean cells.
    def cleanPercentage(self):

        totalCells = self.width * self.height

        return (
            (totalCells - len(self.dirtyCells))
            / totalCells * 100
        )

    # Collects the final simulation statistics.
    # Parameters: None.
    # Returns: Dictionary containing simulation results.
    def getStats(self):

        if self.completionTime is not None:
            executionTime = self.completionTime
        else:
            executionTime = self.currentStep

        return {
            "executionTime": executionTime,
            "cleanedPercentage": self.cleanPercentage(),
            "remainingDirtyCells": len(self.dirtyCells),
            "totalMoves": self.totalMoves,
            "allClean": self.completionTime is not None
        }
