# A script to ask for and store relevant information about the runner

# This function checks whether the user's input matches one of the allowed options.
# It keeps asking until the user enters a valid response.
def get_valid_choice(prompt, valid_options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        else:
            print(f"Invalid input. Please choose from: {', '.join(valid_options)}")


# This function makes sure the user enters a positive whole number.
def get_positive_int(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit():
            value = int(user_input)
            if value > 0:
                return value
        print("Invalid input. Please enter a positive whole number.")


# This function makes sure the user enters a positive number.
# It works for inputs like 3, 4.5, etc.
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


# This function asks the user for a weekday and checks that it is valid.
def get_weekday(prompt):
    valid_days = [
        "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday"
    ]
    day = get_valid_choice(prompt, valid_days)
    return day.capitalize()


# This function asks for the runner's main goal.
# Right now, the goal can either be to finish or to improve time.
def get_goal():
    valid_goals = ["finish", "improve time"]
    return get_valid_choice(
        "What is your goal? (finish / improve time): ",
        valid_goals
    )


# This function makes sure the user enters a realistic number of running days per week.
def get_running_days():
    while True:
        days = get_positive_int("How many days per week can you run? ")
        if 1 <= days <= 7:
            return days
        print("Invalid input. Please enter a number from 1 to 7.")


# This function asks the user for their average pace in minutes per mile.
# For example, 9.5 means 9 minutes and 30 seconds per mile.
def get_average_pace():
    print("Please enter your average pace in minutes per mile.")
    print("For example, enter 9.5 for 9 minutes 30 seconds per mile.")
    return get_positive_float("Average pace: ")


# If the user wants to improve their time, this function asks for a finish time goal.
# The time must be entered in hours:minutes:seconds format.
def get_time_goal():
    while True:
        time_goal = input("What is your goal finish time? (hours:minutes:seconds): ").strip()
        parts = time_goal.split(":")

        if len(parts) == 3:
            hours, minutes, seconds = parts

            if hours.isdigit() and minutes.isdigit() and seconds.isdigit():
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)

                if minutes < 60 and seconds < 60:
                    return f"{hours}:{minutes:02}:{seconds:02}"

        print("Invalid input. Please enter the time in hours:minutes:seconds format, like 4:15:00.")


# This main function asks for and stores the runner's information.
# It uses the helper functions above to make sure the inputs are valid.
def get_runner_info():
    """
    Ask the user for basic marathon training information.
    Returns a dictionary containing the user's inputs.
    """
    print("Welcome to the Marathon Training Plan Generator!")
    print("Please answer the following questions.\n")

    # Ask for the runner's current training background.
    weekly_mileage = get_positive_float(
        "How many miles are you currently running per week? "
    )
    longest_run = get_positive_float("What is your longest recent run (in miles)? ")
    average_pace = get_average_pace()
    running_days = get_running_days()
    weeks_until_race = get_positive_int("How many weeks until your race? ")
    goal = get_goal()

    # Only ask for a goal finish time if the runner wants to improve time.
    time_goal = None
    if goal == "improve time":
        time_goal = get_time_goal()

    # Ask whether the runner needs any specific off days.
    off_days = []
    needs_off_days = get_valid_choice(
        "Do you need any specific days off? (yes/no): ",
        ["yes", "no"]
    )

    if needs_off_days == "yes":
        # The maximum number of off days depends on how many days the user wants to run.
        max_off_days = 7 - running_days
        while True:
            num_off_days = get_positive_int("How many specific off days do you need? ")
            if num_off_days <= max_off_days:
                break
            print(f"You can choose at most {max_off_days} off days based on your available running days.")

        # Ask for each off day and make sure there are no duplicates.
        for i in range(num_off_days):
            day = get_weekday(f"Enter off day #{i + 1}: ")
            while day in off_days:
                print("You already entered that day.")
                day = get_weekday(f"Enter a different off day #{i + 1}: ")
            off_days.append(day)

    # Ask which day the runner prefers for the long run.
    long_run_day = get_weekday("What day would be best for your long run? ")

    # The long run day cannot also be an off day.
    while long_run_day in off_days:
        print("That day is already listed as an off day.")
        long_run_day = get_weekday("Please choose a different day for your long run: ")

    # Store all runner information in a dictionary and return it.
    return {
        "weekly_mileage": weekly_mileage,
        "longest_run": longest_run,
        "average_pace": average_pace,
        "running_days": running_days,
        "weeks_until_race": weeks_until_race,
        "goal": goal,
        "time_goal": time_goal,
        "off_days": off_days,
        "long_run_day": long_run_day
    }


