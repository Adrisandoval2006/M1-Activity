"""
Runs  cleaning robot experiments and saves results.
Authors: Adriana Sandoval Santos - A01667445
         Marbella Barba De los Santos - A01660946
         Javier Padilla Marcial - A01660945
         Camila Quintanilla Cabrera - A01662397
         Alani Daniel Garcia Maya - A01277308
Date: 2026-11-13
"""

import csv
from Model import CleaningModel

TESTS = [
    {"name": "1 agent", "numAgents": 1, "width": 10,
     "height": 10, "dirtyPercentage": 30,
     "maxSteps": 100, "repetitions": 100},

    {"name": "5 agents", "numAgents": 5, "width": 10,
     "height": 10, "dirtyPercentage": 30,
     "maxSteps": 100, "repetitions": 100},

    {"name": "7 agents", "numAgents": 7, "width": 10,
     "height": 10, "dirtyPercentage": 30,
     "maxSteps": 100, "repetitions": 100},

    {"name": "10 agents", "numAgents": 10, "width": 10,
     "height": 10, "dirtyPercentage": 30,
     "maxSteps": 100, "repetitions": 100}
]

OUTPUT_FILE = "test_results.csv"

COLUMNS = [
    "test", "run", "seed", "numAgents",
    "width", "height", "dirtyPercentage",
    "maxSteps", "executionTime",
    "cleanedPercentage", "remainingDirtyCells",
    "totalMoves", "allClean"
]

# Executes one simulation with the specified parameters.
# Parameters:
# test: Dictionary containing experiment settings.
# run: Current repetition number.
# seed: Random seed for reproducibility.
# Returns: Dictionary with simulation statistics.
def runTest(test, run, seed):

    model = CleaningModel(
        dirtyPercentage=test["dirtyPercentage"],
        maxSteps=test["maxSteps"],
        numAgents=test["numAgents"],
        width=test["width"],
        height=test["height"],
        seed=seed
    )

    while model.running:
        model.step()

    row = {
        "test": test["name"],
        "run": run,
        "seed": seed,
        "numAgents": test["numAgents"],
        "width": test["width"],
        "height": test["height"],
        "dirtyPercentage": test["dirtyPercentage"],
        "maxSteps": test["maxSteps"]
    }

    row.update(model.getStats())

    return row

# Runs all experiments and collects their results.
# Parameters:
# tests: List of experiment configurations.
# Returns: List of dictionaries containing results.
def runAll(tests):

    rows = []

    for test in tests:
        for run in range(1, test["repetitions"] + 1):
            seed = test.get("seedStart", 0) + run - 1
            rows.append(runTest(test, run, seed))

        print(
            f"Test '{test['name']}' completed "
            f"({test['repetitions']} runs)"
        )

    return rows

# Saves experiment results to a CSV file.
# Parameters:
# rows: List of result dictionaries.
# path: Output file location.
# Returns: None.
def saveCsv(rows, path):

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print("CSV saved to:", path)

# Executes all experiments and exports their results.
# Parameters: None.
# Returns: None.
def main():

    rows = runAll(TESTS)
    saveCsv(rows, OUTPUT_FILE)

if __name__ == "__main__":
    main()
