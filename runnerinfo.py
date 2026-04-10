# A script to ask for and store relevant information about the runner

# First, we define a series of functions that are used to validate our runners input info in the get_runner_info() function.
# These functions use a loop to continue asking for input from the user until they input a valid input.
def get_valid_choice(prompt, valid_options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        else:
            print(f"Invalid input. Please choose from: {', '.join(valid_options)}")


def get_positive_int(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit():
            value = int(user_input)
            if value > 0:
                return value
        print("Invalid input. Please enter a positive whole number.")


def get_positive_float(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            value = float(user_input)
            if value > 0:
                return value
            else:
                print("Invalid input. Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_experience_level():
    valid_levels = ["beginner", "intermediate"]
    return get_valid_choice(
        "What is your experience level? (beginner/intermediate): ",
        valid_levels
    )

def get_weekday(prompt):
    valid_days = [
        "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday"
    ]
    day = get_valid_choice(prompt, valid_days)
    return day.capitalize()

def get_running_days():
    '''
    makes sure number of running days input is realistic
    '''
    while True:
        days = get_positive_int("How many days per week can you run? ")
        if 1 <= days <= 7:
            return days
        print("Invalid input. Please enter a number from 1 to 7.")

def get_goal():
    valid_goals = ["finish", "improve time", "first marathon"]
    return get_valid_choice(
        "What is your goal? (finish / improve time / first marathon): ",
        valid_goals
    )

# This function retrieves and stores the information about the runner. It calls all of the above functions in doing so to ensure runner inputs are valid.
def get_runner_info():
    """
    Ask the user for basic marathon training information.
    Returns a dictionary containing the user's inputs.
    """
    print("Welcome to the Marathon Training Plan Generator!")
    print("Please answer the following questions.\n")

    weekly_mileage = get_positive_float("What is your current weekly mileage? ")
    longest_run = get_positive_float("What is your longest recent run (in miles)? ")
    running_days = get_running_days()
    weeks_until_race = get_positive_int("How many weeks until your race? ")
    goal = get_goal()
    experience = get_experience_level()

    off_days = []
    needs_off_days = get_valid_choice(
        "Do you need any specific days off? (yes/no): ",
        ["yes", "no"]
    )

    if needs_off_days == "yes":
        num_off_days = get_positive_int("How many specific off days do you need? ")
        for i in range(num_off_days):
            day = get_weekday(f"Enter off day #{i + 1}: ")
            while day in off_days:
                print("You already entered that day.")
                day = get_weekday(f"Enter a different off day #{i + 1}: ")
            off_days.append(day)

    long_run_day = get_weekday("What day would be best for your long run? ")

    return {
        "weekly_mileage": weekly_mileage,
        "longest_run": longest_run,
        "running_days": running_days,
        "weeks_until_race": weeks_until_race,
        "goal": goal,
        "experience": experience,
        "off_days": off_days,
        "long_run_day": long_run_day
    }

# NOTE: this is a sample week, and is not yet personalized. It is just meant to give an idea of what the printed weekly schedules will look like, and will likely
# be completely overwritten in the future.
def generate_sample_week(runner_info):
    """
    Generates a simple sample week based on the runner's input.
    Returns a dictionary with days of the week as keys and workouts as values.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Start by making every day a rest day
    schedule = {}
    for day in days:
        schedule[day] = "Rest"

    running_days = runner_info["running_days"]
    off_days = runner_info["off_days"]
    long_run_day = runner_info["long_run_day"]
    weekly_mileage = runner_info["weekly_mileage"]
    longest_run = runner_info["longest_run"]

    # Put required off days into the schedule
    for day in off_days:
        schedule[day] = "Rest"

    # Choose a simple long run distance
    long_run_miles = longest_run + 1
    if long_run_miles > weekly_mileage / 2:
        long_run_miles = round(weekly_mileage / 2, 1)
    if long_run_miles < 3:
        long_run_miles = 3

    schedule[long_run_day] = f"{long_run_miles} mile long run"

    # Figure out how many other run days are needed
    other_runs_needed = running_days - 1

    # Find days available for other runs
    available_days = []
    for day in days:
        if day != long_run_day and day not in off_days:
            available_days.append(day)

    # Assign easy runs to the first available days
    other_run_days = available_days[:other_runs_needed]

    remaining_miles = weekly_mileage - long_run_miles
    if other_runs_needed > 0:
        easy_run_miles = round(remaining_miles / other_runs_needed, 1)
    else:
        easy_run_miles = 0

    for day in other_run_days:
        schedule[day] = f"{easy_run_miles} mile easy run"

    return schedule


def print_sample_week(schedule, week_num):
    """
    Prints the sample week in a clean format.
    """
    print(f'\n----- SAMPLE WEEK {week_num} PLAN -----')
    for day, workout in schedule.items():
        print(f"{day}: {workout}")


runner_info = get_runner_info()
print("\nRunner info collected successfully:")
print(runner_info)

sample_week1 = generate_sample_week(runner_info)
print_sample_week(sample_week1, 1)
