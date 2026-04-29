# This is the file that handles the data about the runner's progress through the current training plan.

# This file updates runner information based on the completed workouts
# from the current week.

# This function uses the workout log to create updated runner info
# for the next week of training.
def update_runner_info(runner_info, workout_log):
    # Start by collecting only completed runs.
    completed_runs = []

    for day, workout_data in workout_log.items():
        if workout_data["completed"]:
            completed_runs.append(workout_data)

    # If no runs were completed, return a slightly adjusted copy
    # that only moves the race one week closer.
    if len(completed_runs) == 0:
        updated_info = runner_info.copy()
        updated_info["weeks_until_race"] = max(1, runner_info["weeks_until_race"] - 1)
        return updated_info

    # Calculate total mileage from completed runs.
    total_mileage = 0
    for run in completed_runs:
        total_mileage += run["actual_distance"]

    # Calculate average pace from completed runs that have a pace entered.
    pace_values = []
    for run in completed_runs:
        if run["actual_pace"] is not None:
            pace_values.append(run["actual_pace"])

    if len(pace_values) > 0:
        average_pace = sum(pace_values) / len(pace_values)
    else:
        average_pace = runner_info["average_pace"]

    # Find the longest completed run.
    longest_run = 0
    for run in completed_runs:
        if run["actual_distance"] > longest_run:
            longest_run = run["actual_distance"]

    # Create an updated copy of runner_info.
    updated_info = runner_info.copy()
    updated_info["weekly_mileage"] = round(total_mileage, 1)
    updated_info["average_pace"] = round(average_pace, 2)
    updated_info["longest_run"] = round(longest_run, 1)
    updated_info["weeks_until_race"] = max(1, runner_info["weeks_until_race"] - 1)

    return updated_info
