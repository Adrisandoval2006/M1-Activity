import csv
from Modelo import CleaningModel

TESTS = [
    {"name": "1 agente", "num_agents": 1, "width": 10, "height": 10,
     "dirty_per": 30, "max_t": 100, "repetitions": 100},
    {"name": "5 agentes", "num_agents": 5, "width": 10, "height": 10,
     "dirty_per": 30, "max_t": 100, "repetitions": 100},
    {"name": "7 agentes", "num_agents": 7, "width": 10, "height": 10,
     "dirty_per": 30, "max_t": 100, "repetitions": 100},
    {"name": "10 agentes", "num_agents": 10, "width": 10, "height": 10,
     "dirty_per": 30, "max_t": 100, "repetitions": 100},
]

OUTPUT_FILE = "resultados_pruebas"

COLUMNS = ["test", "run", "seed", "num_agents", "width", "height",
           "dirty_per", "max_t", "execution_time", "cleaned_percentage",
           "remaining_dirty_cells", "total_moves", "all_clean"]


def run_test(test, run, seed):
    model = CleaningModel(
        dirty_per=test["dirty_per"],
        max_t=test["max_t"],
        num_agents=test["num_agents"],
        width=test["width"],
        height=test["height"],
        rng=seed,
    )
    while model.running:
        model.step()

    row = {
        "test": test["name"],
        "run": run,
        "seed": seed,
        "num_agents": test["num_agents"],
        "width": test["width"],
        "height": test["height"],
        "dirty_per": test["dirty_per"],
        "max_t": test["max_t"],
    }
    row.update(model.get_stats())
    return row


def run_all(tests):
    '''Runs all tests and returns the list of rows'''
    
    rows = []
    for test in tests:
        for run in range(1, test["repetitions"] + 1):
            seed = test.get("seed_start", 0) + run - 1
            rows.append(run_test(test, run, seed))
        print(f"Prueba '{test['name']}' terminada "
              f"({test['repetitions']} corridas)")
    return rows


def save_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print("CSV guardado en", path)

def main():
    rows = run_all(TESTS)
    save_csv(rows, OUTPUT_FILE + ".csv")

main()