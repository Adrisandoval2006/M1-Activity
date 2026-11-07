
from Modelo import CleaningModel

model = CleaningModel(
    dirty_per=30,
    max_t=100,
    num_agentes=7,
    width=10,
    height=10
)

while model.start_step < model.max_t and model.dirty_cells:
    model.step()

print("\nSimulation results:")
print(model.get_stats())
