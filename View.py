"""
Runs multiple cleaning robot experiments and saves results.
Authors: Adriana Sandoval Santos - A01667445
         Marbella Barba De los Santos - A01660946
         Javier Padilla Marcial - A01660945
         Camila Quintanilla Cabrera - A01662397
         Alani Daniel Garcia Maya - A01277308
Date: 2026-11-13
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
from Model import CleaningModel

ROOM_WIDTH = 10
ROOM_HEIGHT = 10
DIRTY_PERCENTAGE = 30
MAX_STEPS = 100
NUM_AGENTS = 1
STEP_DELAY = 0.15


# Draws the current dirty cells and robot locations on the plot.
# Parameters: axes: Matplotlib axes; model: Current simulation model.
# Returns: None.
def drawRoom(axes, model):
    axes.clear()

    colors = [
        [
            1 if (x, y) in model.dirtyCells else 0
            for x in range(model.width)
        ]
        for y in range(model.height)
    ]

    axes.imshow(
        colors,
        origin="lower",
        interpolation="nearest",
        cmap=ListedColormap(["#86EFAC", "#9CA3AF"]),
        vmin=0,
        vmax=1
    )

    for agent in model.agents:
        axes.plot(
            agent.pos[0],
            agent.pos[1],
            "o",
            color="#2563EB",
            markersize=8,
            markeredgecolor="white"
        )

    axes.set_xticks(range(model.width))
    axes.set_yticks(range(model.height))

    axes.set_xticks(
        [value - 0.5 for value in range(model.width + 1)],
        minor=True
    )

    axes.set_yticks(
        [value - 0.5 for value in range(model.height + 1)],
        minor=True
    )

    axes.grid(which="minor", color="white", linewidth=1)
    axes.tick_params(which="minor", bottom=False, left=False)

    axes.set_title(
        f"Step: {model.currentStep}/{model.maxSteps} | "
        f"Clean: {model.cleanPercentage():.1f}% | "
        f"Moves: {model.totalMoves}"
    )


# Starts the interactive visualization and runs the simulation.
# Parameters: None.
# Returns: None.
def main():
    model = CleaningModel(
        dirtyPercentage=DIRTY_PERCENTAGE,
        maxSteps=MAX_STEPS,
        numAgents=NUM_AGENTS,
        width=ROOM_WIDTH,
        height=ROOM_HEIGHT
    )

    figure, axes = plt.subplots(figsize=(9, 6))
    plt.subplots_adjust(bottom=0.16)

    buttonAxes = figure.add_axes(
        (0.42, 0.04, 0.16, 0.07)
    )

    pauseButton = Button(
        buttonAxes,
        "Pause / Play"
    )

    state = {"paused": False}

    # Toggles the animation when the button is clicked.
    # Parameters: event: Matplotlib button event.
    # Returns: None.
    def togglePause(event):
        state["paused"] = not state["paused"]

    pauseButton.on_clicked(togglePause)

    drawRoom(axes, model)
    plt.show(block=False)

    while plt.fignum_exists(figure.number) and model.running:
        plt.pause(STEP_DELAY)

        if not state["paused"]:
            model.step()
            drawRoom(axes, model)
            figure.canvas.draw_idle()

    if plt.fignum_exists(figure.number):
        drawRoom(axes, model)
        plt.show()


if __name__ == "__main__":
    main()