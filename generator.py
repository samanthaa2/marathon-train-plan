# A file where the behind the scenes calculations for the plan are conducted


### PART 1: STATIC INPUTS TO CREATE INITIAL PLAN

# This function converts a pace in minutes-per-mile form (like 9.5)
# into a readable string like 9:30/mile.
# Useful for readability of printouts
def format_pace(pace):
    minutes = int(pace)
    seconds = round((pace - minutes) * 60)

    # Handle the case where rounding gives 60 seconds.
    if seconds == 60:
        minutes += 1
        seconds = 0

    return f"{minutes}:{seconds:02}/mile"

# this function defines pace target windows for the first week based on the initial information presented
# the pace target windows are spread across 3 workout types: easy run, long run, and workout
# returns pace targets as a dictionary
def init_pace_targets(runnerinfo):
    average_pace = runnerinfo["average_pace"]

    # easy runs and long runs should aim slower than average pace; workout runs are faster
    # NOTE: these only apply to the construction of the initial plan, which considers potential inconsistencies
    # or exaggeration in the information provided by the user
    pace_targets = {
        "easy": (format_pace(average_pace+.5),
                 format_pace(average_pace + 1.5)
        ),
        "long": (format_pace(average_pace + .75),
                 format_pace(average_pace + 1.75)
        ),
        "workout": (
            format_pace(max(average_pace - 0.25, 0.1)),
            format_pace(average_pace + 0.25)
        )
    }

    return pace_targets


# This function decides whether the runner should get a workout day.
# Finish-focused plans are more conservative.
def should_include_workout(runner_info):
    goal = runner_info["goal"]
    running_days = runner_info["running_days"]
    weekly_mileage = runner_info["weekly_mileage"]
    weeks_until_race = runner_info["weeks_until_race"]

    if goal == "finish":
        return running_days >= 5 and weekly_mileage >= 20 and weeks_until_race >= 8

    if goal == "improve time":
        return running_days >= 4 and weekly_mileage >= 15 and weeks_until_race >= 6

    return False



