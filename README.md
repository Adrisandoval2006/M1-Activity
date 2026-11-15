# M1-Activity

## Project Description

This project simulates a multi-agent cleaning system using Python and the Mesa framework.

The objective is to analyze how the number of cleaning robots affects the time required to clean a room and the total number of movements performed.

The simulation takes place in an *M×N* room with randomly distributed dirty cells. Each robot follows a simple set of rules: if its current cell is dirty, it cleans it; otherwise, it randomly attempts to move to one of the eight neighboring cells.

The simulation ends when all cells are clean or when the maximum number of steps is reached.

## Dependencies

- Python 3.11
- Mesa 3.x
- Pandas
- Matplotlib
- Jupyter Notebook

## Project Files

- `Agent.py`: Defines the cleaning robots and their behavior.
- `Model.py`: Manages the room, agents, and simulation statistics.
- `Test.py`: Runs experiments and saves the results in CSV files.
- `View.py`: Displays a visualization of the cleaning process.
- `Analysis.ipynb`: Contains the experimental analysis, graphs, and conclusions.

## How to Run

To visualize the simulation:

```
python3 View.py
```

To execute the experiments:

```
python3 Test.py
```

To review the analysis, open `Analysis.ipynb` in Jupyter Notebook or VS Code and execute the cells.

## Authors

* Adriana Sandoval Santos - A01667445
* Marbella Barba De los Santos - A01660946
* Javier Padilla Marcial - A01660945
* Camila Quintanilla Cabrera - A01662397
* Alani Daniel Garcia Maya - A01277308