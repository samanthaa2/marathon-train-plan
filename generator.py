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






