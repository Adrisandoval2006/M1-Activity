"""
Runs multiple cleaning robot experiments and saves results.
Authors: Adriana Sandoval Santos - A01667445
         Marbella Barba De los Santos - A01660946
         Javier Padilla Marcial - A01660945
         Camila Quintanilla Cabrera - A01662397
         Alani Daniel Garcia Maya - A01277308
Date: 2026-11-13
"""

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from Model import CleaningModel


ROOM_WIDTH = 15
ROOM_HEIGHT = 15
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500


# Defines the visual appearance of each robot.
# Parameters:
# agent: Robot agent to be displayed.
# Returns: Dictionary containing visual properties.
def robotPortrayal(agent):

    return {
        "Shape": "circle",
        "Color": "#2563EB",
        "Filled": "true",
        "Layer": 1,
        "r": 0.35
    }


class CleaningGrid(CanvasGrid):

    # Draws dirty and clean cells behind the robots.
    # Parameters:
    # model: Current cleaning simulation model.
    # Returns: Dictionary containing visualization data.
    def render(self, model):

        gridData = super().render(model)
        cells = []

        for x in range(model.width):
            for y in range(model.height):

                if (x, y) in model.dirtyCells:
                    color = "#9CA3AF"
                else:
                    color = "#86EFAC"

                cells.append({
                    "Shape": "rect",
                    "Color": color,
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1,
                    "x": x,
                    "y": y
                })

        gridData[0] = cells

        return gridData


# Creates and launches the visualization server.
# Parameters: None.
# Returns: None.
def main():

    grid = CleaningGrid(
        robotPortrayal,
        ROOM_WIDTH,
        ROOM_HEIGHT,
        CANVAS_WIDTH,
        CANVAS_HEIGHT
    )

    modelParams = {
        "dirtyPercentage": Slider(
            "Dirty cells (%)",
            30,
            0,
            100,
            5
        ),
        "maxSteps": Slider(
            "Maximum steps",
            100,
            10,
            1000,
            10
        ),
        "numAgents": Slider(
            "Number of robots",
            7,
            1,
            20,
            1
        ),
        "width": ROOM_WIDTH,
        "height": ROOM_HEIGHT
    }

    server = ModularServer(
        CleaningModel,
        [grid],
        "Reactive Cleaning Robots",
        modelParams
    )

    server.port = 8521
    server.launch()


if __name__ == "__main__":
    main()
