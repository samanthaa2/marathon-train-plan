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


# This function chooses a reasonable long run distance.
# It starts near the runner's current longest run and builds slightly.
def choose_long_run_distance(runner_info):
    weekly_mileage = runner_info["weekly_mileage"]
    longest_run = runner_info["longest_run"]
    weeks_until_race = runner_info["weeks_until_race"]

    long_run = longest_run + 1

    # Keep the long run from becoming too large compared to total weekly mileage.
    max_long_run = weekly_mileage * 0.45
    if long_run > max_long_run:
        long_run = max_long_run

    # If there is not much time until the race, stay more conservative.
    if weeks_until_race < 6:
        long_run = min(long_run, longest_run)

    # Keep a minimum long run distance for the plan.
    if long_run < 3:
        long_run = 3

    return round(long_run, 1)

# This function chooses a target weekly mileage for the baseline week.
# For now, it mostly keeps the runner near their current mileage.
def choose_weekly_mileage(runner_info):
    weekly_mileage = runner_info["weekly_mileage"]
    weeks_until_race = runner_info["weeks_until_race"]

    # Build slightly if there is enough time.
    if weeks_until_race >= 10:
        weekly_mileage *= 1.05

    return round(weekly_mileage, 1)

# This function returns the day before a given weekday.
def get_previous_day(day):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    index = days.index(day)
    return days[index - 1]

# This function returns the day after a given weekday.
def get_next_day(day):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    index = days.index(day)
    return days[(index + 1) % len(days)]

# this function assigns workouts to specific days for the first week
# it takes into account rest days and long run days, and attempts to optimize spacing
def choose_workout_day(runnerinfo):
