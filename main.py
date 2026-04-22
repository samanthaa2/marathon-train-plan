# the file where the code is run

# first, import relative functions
from runner_info import get_runner_info
from plan_generator import generate_baseline_week, print_week_plan

runner_info = get_runner_info()

print("\nRunner information:")
print(runner_info)

baseline_week = generate_baseline_week(runner_info)
print_week_plan(baseline_week)
