
from Modelo import CleaningModel

model = CleaningModel(
    dirty_per=30,
    max_t=100,
    num_agents=7,
    width=10,
    height=10
)

while model.running:
    model.step()

print("\nSimulation results:")
print(model.get_stats())
