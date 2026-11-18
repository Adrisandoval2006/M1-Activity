import csv
import time
from Model import CleaningModel

TESTS = [
    {"name": "1 agent", "numAgents": 1, "width": 10, "height": 10,
     "dirtyPercentage": 30, "maxSteps": 100, "repetitions": 100},
    {"name": "5 agents", "numAgents": 5, "width": 10, "height": 10,
     "dirtyPercentage": 30, "maxSteps": 100, "repetitions": 100},
    {"name": "7 agents", "numAgents": 7, "width": 10, "height": 10,
     "dirtyPercentage": 30, "maxSteps": 100, "repetitions": 100},
    {"name": "10 agents", "numAgents": 10, "width": 10, "height": 10,
     "dirtyPercentage": 30, "maxSteps": 100, "repetitions": 100},

    # Long run
    {"name": "1 agent long run", "numAgents": 1, "width": 10,
     "height": 10, "dirtyPercentage": 30, "maxSteps": 10000,
     "repetitions": 100},
    {"name": "5 agents long run", "numAgents": 5, "width": 10,
     "height": 10, "dirtyPercentage": 30, "maxSteps": 10000,
     "repetitions": 100},
    {"name": "7 agents long run", "numAgents": 7, "width": 10,
     "height": 10, "dirtyPercentage": 30, "maxSteps": 10000,
     "repetitions": 100},
    {"name": "10 agents long run", "numAgents": 10, "width": 10,
     "height": 10, "dirtyPercentage": 30, "maxSteps": 10000,
     "repetitions": 100},
]

OUTPUT_FILE = "test_results.csv"
AGENT_OUTPUT_FILE = "agent_results.csv"

COLUMNS = ["test", "run", "seed", "numAgents", "width", "height",
           "dirtyPercentage", "maxSteps", "executionTime", "completionTime",
           "cleanedPercentage", "remainingDirtyCells", "totalMoves",
           "allClean", "runTimeS"]

AGENT_COLUMNS = ["test", "run", "seed", "numAgents", "agentId",
                 "activeSteps", "movements", "cellsCleaned"]

def runTest(test, run, seed):
    startTime = time.perf_counter()

    model = CleaningModel(
        dirtyPercentage=test["dirtyPercentage"],
        maxSteps=test["maxSteps"],
        numAgents=test["numAgents"],
        width=test["width"],
        height=test["height"],
        seed=seed,
    )
    while model.running:
        model.step()

    runTime = time.perf_counter() - startTime

    row = {
        "test": test["name"],
        "run": run,
        "seed": seed,
        "numAgents": test["numAgents"],
        "width": test["width"],
        "height": test["height"],
        "dirtyPercentage": test["dirtyPercentage"],
    }
    row.update(model.getStats())  # includes maxSteps
    row["runTimeS"] = round(runTime, 6)

    agentRows = []
    for agentStats in model.getAgentStats():
        agentRow = {
            "test": test["name"],
            "run": run,
            "seed": seed,
            "numAgents": test["numAgents"],
        }
        agentRow.update(agentStats)
        agentRows.append(agentRow)

    return row, agentRows

def runAll(tests):
    summaries = []
    agentRows = []
    for test in tests:
        for run in range(1, test["repetitions"] + 1):
            seed = test.get("seedStart", 0) + run - 1
            row, robots = runTest(test, run, seed)
            summaries.append(row)
            agentRows.extend(robots)
        print(f"Prueba '{test['name']}' terminada "
              f"({test['repetitions']} corridas)")
    return summaries, agentRows


def saveCsv(rows, path, columns):
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print("CSV saved on", path)


def main():
    summaries, agentRows = runAll(TESTS)
    saveCsv(summaries, OUTPUT_FILE, COLUMNS)

main()