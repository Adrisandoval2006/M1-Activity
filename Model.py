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
    # Creates a room, dirty cells, and robots for one simulation.
    # Parameters: dirtyPercentage: Percentage of initially dirty cells.
    # maxSteps: Maximum number of simulation steps.
    # numAgents: Number of robots.
    # width: Number of columns; height: Number of rows.
    # seed: Optional random seed for reproducibility.
    # Returns: None.
    def __init__(self, dirtyPercentage, maxSteps, numAgents=7,
                 width=10, height=10, seed=None):
        super().__init__(seed=seed)

        if not 0 <= dirtyPercentage <= 100:
            raise ValueError("Dirty percentage must be between 0 and 100")
        if width <= 0 or height <= 0:
            raise ValueError("Room dimensions must be positive")
        if numAgents <= 0:
            raise ValueError("Number of agents must be positive")
        if maxSteps < 0:
            raise ValueError("Maximum steps cannot be negative")

        self.dirtyPercentage = dirtyPercentage
        self.maxSteps = maxSteps
        self.numAgents = numAgents
        self.width = width
        self.height = height
        self.currentStep = 0
        self.totalMoves = 0
        self.completionTime = None

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
        self.initialDirtyCells = numDirtyCells

        for _ in range(numAgents):
            agent = RobotAgent(self)
            self.grid.place_agent(agent, (0, 0))

        self.running = bool(self.dirtyCells) and maxSteps > 0

        if not self.dirtyCells:
            self.completionTime = 0

    # Activates every robot once and updates simulation time.
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

    # Calculates the percentage of cells that are clean.
    # Parameters: None.
    # Returns: Float representing the clean percentage.
    def cleanPercentage(self):
        totalCells = self.width * self.height
        return 100 * (totalCells - len(self.dirtyCells)) / totalCells

    # Returns the per-robot counters for the current simulation.
    # Parameters: None.
    # Returns: List of dictionaries with each robot's statistics.
    def getAgentStats(self):
        agentStats = []
        
        for agent in self.agents:
            agentStats.append({
                "agentId": agent.unique_id,
                "activeSteps": agent.actions,
                "movements": agent.movements,
                "cellsCleaned": agent.cellsCleaned
            })
            
        return agentStats

    # Returns overall statistics for the current simulation.
    # Parameters: None.
    # Returns: Dictionary of simulation-level measurements.
    def getStats(self):
        return {
            "executionTime": self.currentStep,
            "completionTime": self.completionTime,
            "maxSteps": self.maxSteps,
            "cleanedPercentage": self.cleanPercentage(),
            "remainingDirtyCells": len(self.dirtyCells),
            "totalMoves": self.totalMoves,
            "allClean": self.completionTime is not None
        }