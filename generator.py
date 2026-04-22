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

# This function tries to place a workout day away from the long run.
def choose_workout_day(runner_info, available_days):
    long_run_day = runner_info["long_run_day"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    day_before_long = get_previous_day(long_run_day, days)
    day_after_long = get_next_day(long_run_day, days)

    good_days = []
    for day in available_days:
        if day != day_before_long and day != day_after_long:
            good_days.append(day)

    # Prefer midweek days if possible.
    preferred_order = ["Tuesday", "Wednesday", "Thursday", "Friday", "Monday", "Saturday"]

    for day in preferred_order:
        if day in good_days:
            return day

    for day in preferred_order:
        if day in available_days:
            return day

    return None


# This function generates a baseline week.
# It returns a dictionary with weekdays as keys and workout descriptions as values.
def generate_baseline_week(runner_info):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    weekly_mileage = choose_weekly_mileage(runner_info)
    long_run_distance = choose_long_run_distance(runner_info)
    long_run_day = runner_info["long_run_day"]
    off_days = runner_info["off_days"]
    running_days = runner_info["running_days"]

    pace_targets = get_pace_targets(runner_info)

    # Start by setting every day to rest.
    schedule = {}
    for day in days:
        schedule[day] = "Rest"

    # Mark required off days first.
    for day in off_days:
        schedule[day] = "Rest"

    # Place the long run.
    long_pace_low, long_pace_high = pace_targets["long"]
    schedule[long_run_day] = (
        f"{long_run_distance} mile long run "
        f"at about {long_pace_low} to {long_pace_high}"
    )

    run_days_used = 1

    # Find days available for more runs.
    available_days = []
    for day in days:
        if day not in off_days and day != long_run_day:
            available_days.append(day)

    # Decide whether to include a workout day.
    workout_day = None
    workout_distance = 0

    if should_include_workout(runner_info):
        workout_day = choose_workout_day(runner_info, available_days)

        if workout_day is not None:
            workout_distance = round(max(3, weekly_mileage * 0.2), 1)
            workout_pace_low, workout_pace_high = pace_targets["workout"]
            schedule[workout_day] = (
                f"{workout_distance} mile workout "
                f"at about {workout_pace_low} to {workout_pace_high}"
            )
            run_days_used += 1
            available_days.remove(workout_day)

    # Figure out how many easy runs remain.
    easy_runs_needed = running_days - run_days_used

    # Choose days for easy runs in weekday order.
    easy_run_days = available_days[:easy_runs_needed]

    # Calculate how many miles remain after assigning long run and workout.
    remaining_miles = weekly_mileage - long_run_distance - workout_distance

    if easy_runs_needed > 0:
        easy_run_distance = round(remaining_miles / easy_runs_needed, 1)
    else:
        easy_run_distance = 0

    # Keep easy runs from dropping too low.
    if easy_runs_needed > 0 and easy_run_distance < 2:
        easy_run_distance = 2

    easy_pace_low, easy_pace_high = pace_targets["easy"]

    for day in easy_run_days:
        schedule[day] = (
            f"{easy_run_distance} mile easy run "
            f"at about {easy_pace_low} to {easy_pace_high}"
        )

    return schedule


# This function prints the generated week in a readable format.
def print_week_plan(schedule):
    print("\n----- BASELINE TRAINING WEEK -----")
    for day, workout in schedule.items():
        print(f"{day}: {workout}")
