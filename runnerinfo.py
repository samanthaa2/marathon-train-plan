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

