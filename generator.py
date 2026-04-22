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


# This function builds the structure of the week by assigning each day a run type.
# It does not assign distances or paces yet.
def build_week_structure(runner_info):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    running_days = runner_info["running_days"]
    off_days = runner_info["off_days"]
    long_run_day = runner_info["long_run_day"]

    # Start with all days set to rest.
    structure = {}
    for day in days:
        structure[day] = "rest"

    # Mark off days as rest.
    for day in off_days:
        structure[day] = "rest"

    # Place the long run first.
    structure[long_run_day] = "long"
    run_days_used = 1

    # Decide whether this runner should get a workout day.
    workout_day = None
    if should_include_workout(runner_info):
        preferred_workout_order = ["Tuesday", "Thursday", "Monday", "Friday", "Saturday", "Sunday", "Wednesday"]

        day_before_long = get_previous_day(long_run_day)
        day_after_long = get_next_day(long_run_day)

        # First try to place the workout away from the long run.
        for day in preferred_workout_order:
            if (
                day != long_run_day
                and day not in off_days
                and day != day_before_long
                and day != day_after_long
                and structure[day] == "rest"
            ):
                workout_day = day
                break

        # If that is not possible, choose the best remaining day.
        if workout_day is None:
            for day in preferred_workout_order:
                if day != long_run_day and day not in off_days and structure[day] == "rest":
                    workout_day = day
                    break

        if workout_day is not None:
            structure[workout_day] = "workout"
            run_days_used += 1

    # Fill the rest of the needed run days with easy runs.
    easy_runs_needed = running_days - run_days_used

    while easy_runs_needed > 0:
        best_day = None
        best_score = None

        for day in days:
            if structure[day] != "rest":
                continue
            if day in off_days:
                continue

            prev_day = get_previous_day(day)
            next_day = get_next_day(day)

            # Count how many neighboring days already have runs.
            neighbor_runs = 0
            if structure[prev_day] != "rest":
                neighbor_runs += 1
            if structure[next_day] != "rest":
                neighbor_runs += 1

            # Lower score is better because it means the run is less crowded.
            score = neighbor_runs

            if best_score is None or score < best_score:
                best_score = score
                best_day = day

        if best_day is None:
            break

        structure[best_day] = "easy"
        easy_runs_needed -= 1

    return structure


# This function generates the full baseline week by taking the weekly structure
# and assigning distances and pace targets to each run.
def generate_baseline_week(runner_info):
    weekly_mileage = choose_weekly_mileage(runner_info)
    long_run_distance = choose_long_run_distance(runner_info)
    pace_targets = init_pace_targets(runner_info)

    structure = build_week_structure(runner_info)

    # Count how many easy runs and workout runs there are.
    easy_days = []
    workout_days = []

    for day, run_type in structure.items():
        if run_type == "easy":
            easy_days.append(day)
        elif run_type == "workout":
            workout_days.append(day)

    # Choose workout distance if there is a workout.
    if len(workout_days) > 0:
        workout_distance = round(max(3, weekly_mileage * 0.2), 1)
    else:
        workout_distance = 0

    # Divide remaining mileage across easy runs.
    remaining_miles = weekly_mileage - long_run_distance - workout_distance

    if len(easy_days) > 0:
        easy_run_distance = round(remaining_miles / len(easy_days), 1)
    else:
        easy_run_distance = 0

    if len(easy_days) > 0 and easy_run_distance < 2:
        easy_run_distance = 2

    # Build the final schedule text.
    final_schedule = {}

    for day, run_type in structure.items():
        if run_type == "rest":
            final_schedule[day] = "Rest"

        elif run_type == "long":
            long_pace_low, long_pace_high = pace_targets["long"]
            final_schedule[day] = (
                f"{long_run_distance} mile long run "
                f"at about {long_pace_low} to {long_pace_high}"
            )

        elif run_type == "workout":
            workout_pace_low, workout_pace_high = pace_targets["workout"]
            final_schedule[day] = (
                f"{workout_distance} mile workout "
                f"at about {workout_pace_low} to {workout_pace_high}"
            )

        elif run_type == "easy":
            easy_pace_low, easy_pace_high = pace_targets["easy"]
            final_schedule[day] = (
                f"{easy_run_distance} mile easy run "
                f"at about {easy_pace_low} to {easy_pace_high}"
            )

    return final_schedule


# This function prints the generated week in a readable format.
def print_week_plan(schedule):
    print("\n----- BASELINE TRAINING WEEK -----")
    for day, workout in schedule.items():
        print(f"{day}: {workout}")
