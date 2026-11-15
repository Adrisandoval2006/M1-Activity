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
    {"name": f"{count} agents", "numAgents": count, "width": 10,
     "height": 10, "dirtyPercentage": 30, "maxSteps": 100,
     "repetitions": 100}
    for count in (1, 5, 7, 10)
]

OUTPUT_FILE = "test_results.csv"
AGENT_OUTPUT_FILE = "agent_results.csv"

COLUMNS = [
    "test", "run", "seed", "numAgents", "width", "height",
    "dirtyPercentage", "maxSteps", "executionTime", "completionTime",
    "cleanedPercentage", "remainingDirtyCells", "totalMoves", "allClean"
]

AGENT_COLUMNS = [
    "test", "run", "seed", "numAgents", "agentId",
    "activeSteps", "movements", "cellsCleaned"
]


# Runs one experiment and collects overall and per-robot results.
# Parameters: test: Experiment configuration; run: Repetition index.
# seed: Random seed for reproducibility.
# Returns: Tuple containing one summary row and individual robot rows.
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

    summary = {
        "test": test["name"],
        "run": run,
        "seed": seed,
        "numAgents": test["numAgents"],
        "width": test["width"],
        "height": test["height"],
        "dirtyPercentage": test["dirtyPercentage"]
    }

    summary.update(model.getStats())

    agentRows = []

    for agentStats in model.getAgentStats():
        agentRow = {
            "test": test["name"],
            "run": run,
            "seed": seed,
            "numAgents": test["numAgents"]
        }

        agentRow.update(agentStats)
        agentRows.append(agentRow)

    if sum(row["movements"] for row in agentRows) != summary["totalMoves"]:
        raise ValueError(
            "Individual movements do not match total movements"
        )

    return summary, agentRows


# Runs every configured experiment and collects all results.
# Parameters: tests: List of experiment configurations.
# Returns: Tuple containing summary rows and per-robot rows.
def runAll(tests):
    summaries = []
    agentRows = []

    for test in tests:
        for run in range(1, test["repetitions"] + 1):
            seed = test.get("seedStart", 0) + run - 1

            summary, robotRows = runTest(test, run, seed)

            summaries.append(summary)
            agentRows.extend(robotRows)

        print(
            f"Completed {test['name']}: "
            f"{test['repetitions']} runs"
        )

    return summaries, agentRows


# Writes a list of dictionaries to a CSV file.
# Parameters: rows: Results to save; path: CSV destination.
# columns: Ordered CSV column names.
# Returns: None.
def saveCsv(rows, path, columns=COLUMNS):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print("Saved:", path)


# Runs all experiments and saves two CSV files.
# Parameters: None.
# Returns: None.
def main():
    summaries, agentRows = runAll(TESTS)

    saveCsv(summaries, OUTPUT_FILE, COLUMNS)
    saveCsv(agentRows, AGENT_OUTPUT_FILE, AGENT_COLUMNS)


if __name__ == "__main__":
    main()