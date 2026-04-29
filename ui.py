import customtkinter as ctk
import tkinter as tk

# Import the function that generates the baseline week from your planning file.
from generator import generate_baseline_week, format_workout

# Set the appearance and color theme of the app.
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main app window.
app = ctk.CTk()
app.title("Marathon Training Plan Generator")
app.geometry("800x650")

# This dictionary stores the user's information as they move through the screens.
runner_info = {}
# this dictionary stores the plan for the current week
current_week_plan = {}
# dictionary that stores workout data for users current training week
workout_log = {}
# variable that stores the current week number for tracking purposes
current_week_number = 1


# -------------------------
# HELPER FUNCTIONS
# -------------------------

# This function hides all screens so only one appears at a time.
def hide_all_frames():
    screen1_frame.pack_forget()
    screen2_frame.pack_forget()
    off_days_frame.pack_forget()
    screen3_frame.pack_forget()
    results_frame.pack_forget()


# These functions show one screen at a time.
def show_screen1():
    hide_all_frames()
    screen1_frame.pack(fill="both", expand=True, padx=20, pady=20)


def show_screen2():
    hide_all_frames()
    screen2_frame.pack(fill="both", expand=True, padx=20, pady=20)


def show_off_days_screen():
    hide_all_frames()
    off_days_frame.pack(fill="both", expand=True, padx=20, pady=20)


def show_screen3():
    hide_all_frames()
    screen3_frame.pack(fill="both", expand=True, padx=20, pady=20)


def show_results():
    hide_all_frames()
    results_frame.pack(fill="both", expand=True, padx=20, pady=20)


# This function shows or hides the time goal input based on the selected goal.
def toggle_time_goal_input(choice):
    if choice == "improve time":
        time_goal_label.pack(pady=(10, 5))
        time_goal_entry.pack(pady=5)
    else:
        time_goal_label.pack_forget()
        time_goal_entry.pack_forget()


# This function decides where the Back button on the goal screen should go.
def go_back_from_screen3():
    if off_days_menu.get() == "yes":
        show_off_days_screen()
    else:
        show_screen2()

# This function creates the workout display on the results screen.
# Run days become buttons, and rest days become labels.
def display_week_plan():
    # Clear old widgets from the workout area.
    for widget in workout_buttons_frame.winfo_children():
        widget.destroy()

    week_title_label.configure(text=f"Week {current_week_number} Plan")

    for day, workout_data in current_week_plan.items():
        workout_type = workout_data["type"]

        if workout_type == "rest":
            day_label = ctk.CTkLabel(
                workout_buttons_frame,
                text=f"{day}: Rest",
                font=("Arial", 16)
            )
            day_label.pack(pady=6)

        else:
            workout_text = format_workout(day, workout_data)

            workout_button = ctk.CTkButton(
                workout_buttons_frame,
                text=workout_text,
                command=lambda d=day: open_log_workout_popup(d),
                width=600,
                height=40
            )
            workout_button.pack(pady=6)


# -------------------------
# NAVIGATION FUNCTIONS
# -------------------------

# Save screen 1 data, then move to screen 2.
def go_to_screen2():
    try:
        runner_info["weekly_mileage"] = float(weekly_mileage_entry.get())
        runner_info["longest_run"] = float(longest_run_entry.get())
        runner_info["average_pace"] = float(average_pace_entry.get())

        screen1_error_label.configure(text="")
        show_screen2()

    except ValueError:
        screen1_error_label.configure(
            text="Please enter valid numbers for all fields."
        )


# Save screen 2 data, then move to the off-days screen or goal screen.
def go_to_screen3():
    try:
        running_days = int(running_days_entry.get())
        weeks_until_race = int(weeks_until_race_entry.get())
        long_run_day = long_run_day_menu.get()

        if running_days < 1 or running_days > 7:
            screen2_error_label.configure(
                text="Running days must be between 1 and 7."
            )
            return

        runner_info["running_days"] = running_days
        runner_info["weeks_until_race"] = weeks_until_race
        runner_info["long_run_day"] = long_run_day

        screen2_error_label.configure(text="")

        # Decide whether to show the off-days screen.
        if off_days_menu.get() == "yes":
            show_off_days_screen()
        else:
            runner_info["off_days"] = []
            show_screen3()

    except ValueError:
        screen2_error_label.configure(
            text="Please enter valid values before continuing."
        )


# Save selected off days, then continue to the goal screen.
def save_off_days_and_continue():
    off_days = []

    if monday_var.get():
        off_days.append("Monday")
    if tuesday_var.get():
        off_days.append("Tuesday")
    if wednesday_var.get():
        off_days.append("Wednesday")
    if thursday_var.get():
        off_days.append("Thursday")
    if friday_var.get():
        off_days.append("Friday")
    if saturday_var.get():
        off_days.append("Saturday")
    if sunday_var.get():
        off_days.append("Sunday")

    long_run_day = runner_info["long_run_day"]
    running_days = runner_info["running_days"]

    if long_run_day in off_days:
        off_days_error_label.configure(
            text="Your long run day cannot also be an off day."
        )
        return

    if len(off_days) > 7 - running_days:
        off_days_error_label.configure(
            text="You selected too many off days for your available running days."
        )
        return

    runner_info["off_days"] = off_days
    off_days_error_label.configure(text="")
    show_screen3()


# This function stores the completed workout data for one day.
def log_workout(day, completed, actual_distance, actual_pace):
    workout_log[day] = {
        "completed": completed,
        "actual_distance": actual_distance,
        "actual_pace": actual_pace
    }

# Save screen 3 data, generate the plan, and show the results.
def generate_plan():
    global current_week_plan, workout_log

    try:
        goal = goal_menu.get()
        runner_info["goal"] = goal

        # Only save a time goal if the user selected improve time.
        if goal == "improve time":
            time_goal = time_goal_entry.get().strip()

            if time_goal == "":
                screen3_error_label.configure(
                    text="Please enter a goal finish time."
                )
                return

            runner_info["time_goal"] = time_goal
        else:
            runner_info["time_goal"] = None

        screen3_error_label.configure(text="")

        # Generate the plan using existing Python logic.
        current_week_plan = generate_baseline_week(runner_info)

        # Clear the old workout log whenever a new week is generated.
        workout_log = {}

        show_results()
        display_week_plan()

    except ValueError:
        screen3_error_label.configure(
            text="Please enter valid goal information."
        )


# -------------------------
# SCREEN 1: CURRENT TRAINING
# -------------------------

screen1_frame = ctk.CTkFrame(app)

screen1_title = ctk.CTkLabel(
    screen1_frame,
    text="Step 1: Current Training",
    font=("Arial", 24)
)
screen1_title.pack(pady=20)

weekly_mileage_label = ctk.CTkLabel(
    screen1_frame,
    text="How many miles are you currently running per week?"
)
weekly_mileage_label.pack(pady=(10, 5))

weekly_mileage_entry = ctk.CTkEntry(screen1_frame, width=250)
weekly_mileage_entry.pack(pady=5)

longest_run_label = ctk.CTkLabel(
    screen1_frame,
    text="What is your longest recent run (in miles)?"
)
longest_run_label.pack(pady=(10, 5))

longest_run_entry = ctk.CTkEntry(screen1_frame, width=250)
longest_run_entry.pack(pady=5)

average_pace_label = ctk.CTkLabel(
    screen1_frame,
    text="What is your average pace in minutes per mile?"
)
average_pace_label.pack(pady=(10, 5))

average_pace_entry = ctk.CTkEntry(screen1_frame, width=250)
average_pace_entry.pack(pady=5)

screen1_error_label = ctk.CTkLabel(
    screen1_frame,
    text="",
    text_color="red"
)
screen1_error_label.pack(pady=10)

screen1_next_button = ctk.CTkButton(
    screen1_frame,
    text="Next",
    command=go_to_screen2
)
screen1_next_button.pack(pady=20)


# -------------------------
# SCREEN 2: SCHEDULE + RACE INFO
# -------------------------

screen2_frame = ctk.CTkFrame(app)

screen2_title = ctk.CTkLabel(
    screen2_frame,
    text="Step 2: Schedule and Race Info",
    font=("Arial", 24)
)
screen2_title.pack(pady=20)

running_days_label = ctk.CTkLabel(
    screen2_frame,
    text="How many days per week can you run?"
)
running_days_label.pack(pady=(10, 5))

running_days_entry = ctk.CTkEntry(screen2_frame, width=250)
running_days_entry.pack(pady=5)

weeks_until_race_label = ctk.CTkLabel(
    screen2_frame,
    text="How many weeks until your race?"
)
weeks_until_race_label.pack(pady=(10, 5))

weeks_until_race_entry = ctk.CTkEntry(screen2_frame, width=250)
weeks_until_race_entry.pack(pady=5)

long_run_day_label = ctk.CTkLabel(
    screen2_frame,
    text="What day would be best for your long run?"
)
long_run_day_label.pack(pady=(10, 5))

long_run_day_menu = ctk.CTkOptionMenu(
    screen2_frame,
    values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    width=250
)
long_run_day_menu.pack(pady=5)

off_days_question_label = ctk.CTkLabel(
    screen2_frame,
    text="Do you have any required off days?"
)
off_days_question_label.pack(pady=(15, 5))

off_days_menu = ctk.CTkOptionMenu(
    screen2_frame,
    values=["no", "yes"],
    width=250
)
off_days_menu.pack(pady=5)

screen2_error_label = ctk.CTkLabel(
    screen2_frame,
    text="",
    text_color="red"
)
screen2_error_label.pack(pady=10)

screen2_back_button = ctk.CTkButton(
    screen2_frame,
    text="Back",
    command=show_screen1
)
screen2_back_button.pack(pady=(10, 5))

screen2_next_button = ctk.CTkButton(
    screen2_frame,
    text="Next",
    command=go_to_screen3
)
screen2_next_button.pack(pady=10)


# -------------------------
# OFF DAYS SCREEN
# -------------------------

off_days_frame = ctk.CTkFrame(app)

off_days_title = ctk.CTkLabel(
    off_days_frame,
    text="Step 3: Required Off Days",
    font=("Arial", 24)
)
off_days_title.pack(pady=20)

off_days_label = ctk.CTkLabel(
    off_days_frame,
    text="Select any days you need to keep free from running:"
)
off_days_label.pack(pady=(10, 10))

# Create checkbox variables.
monday_var = tk.BooleanVar()
tuesday_var = tk.BooleanVar()
wednesday_var = tk.BooleanVar()
thursday_var = tk.BooleanVar()
friday_var = tk.BooleanVar()
saturday_var = tk.BooleanVar()
sunday_var = tk.BooleanVar()

monday_check = ctk.CTkCheckBox(off_days_frame, text="Monday", variable=monday_var)
monday_check.pack(anchor="w", padx=40, pady=2)

tuesday_check = ctk.CTkCheckBox(off_days_frame, text="Tuesday", variable=tuesday_var)
tuesday_check.pack(anchor="w", padx=40, pady=2)

wednesday_check = ctk.CTkCheckBox(off_days_frame, text="Wednesday", variable=wednesday_var)
wednesday_check.pack(anchor="w", padx=40, pady=2)

thursday_check = ctk.CTkCheckBox(off_days_frame, text="Thursday", variable=thursday_var)
thursday_check.pack(anchor="w", padx=40, pady=2)

friday_check = ctk.CTkCheckBox(off_days_frame, text="Friday", variable=friday_var)
friday_check.pack(anchor="w", padx=40, pady=2)

saturday_check = ctk.CTkCheckBox(off_days_frame, text="Saturday", variable=saturday_var)
saturday_check.pack(anchor="w", padx=40, pady=2)

sunday_check = ctk.CTkCheckBox(off_days_frame, text="Sunday", variable=sunday_var)
sunday_check.pack(anchor="w", padx=40, pady=2)

off_days_error_label = ctk.CTkLabel(
    off_days_frame,
    text="",
    text_color="red"
)
off_days_error_label.pack(pady=10)

off_days_back_button = ctk.CTkButton(
    off_days_frame,
    text="Back",
    command=show_screen2
)
off_days_back_button.pack(pady=(10, 5))

off_days_next_button = ctk.CTkButton(
    off_days_frame,
    text="Next",
    command=save_off_days_and_continue
)
off_days_next_button.pack(pady=10)


# -------------------------
# SCREEN 3: GOAL
# -------------------------

screen3_frame = ctk.CTkFrame(app)

screen3_title = ctk.CTkLabel(
    screen3_frame,
    text="Step 4: Goal",
    font=("Arial", 24)
)
screen3_title.pack(pady=20)

goal_label = ctk.CTkLabel(
    screen3_frame,
    text="What is your goal?"
)
goal_label.pack(pady=(10, 5))

goal_menu = ctk.CTkOptionMenu(
    screen3_frame,
    values=["finish", "improve time"],
    width=250,
    command=toggle_time_goal_input
)
goal_menu.pack(pady=5)

# These widgets will be shown only if "improve time" is selected.
time_goal_label = ctk.CTkLabel(
    screen3_frame,
    text="What is your goal finish time? (hh:mm:ss)"
)

time_goal_entry = ctk.CTkEntry(
    screen3_frame,
    width=250
)

screen3_error_label = ctk.CTkLabel(
    screen3_frame,
    text="",
    text_color="red"
)
screen3_error_label.pack(pady=10)

screen3_back_button = ctk.CTkButton(
    screen3_frame,
    text="Back",
    command=go_back_from_screen3
)
screen3_back_button.pack(pady=(10, 5))

screen3_generate_button = ctk.CTkButton(
    screen3_frame,
    text="Generate Week 1 Plan",
    command=generate_plan
)
screen3_generate_button.pack(pady=10)


# -------------------------
# RESULTS SCREEN
# -------------------------

results_frame = ctk.CTkFrame(app)

week_title_label = ctk.CTkLabel(
    results_frame,
    text="Week 1 Plan",
    font=("Arial", 24)
)
week_title_label.pack(pady=20)

workout_buttons_frame = ctk.CTkFrame(results_frame)
workout_buttons_frame.pack(pady=20, fill="both", expand=True)

results_back_button = ctk.CTkButton(
    results_frame,
    text="Back to Step 1",
    command=show_screen1
)
results_back_button.pack(pady=10)

# -------------------------
# WORKOUT DISPLAY
# -------------------------

# This function opens a popup window so the user can log workout results for one day.
def open_log_workout_popup(day):
    popup = ctk.CTkToplevel(app)
    popup.title(f"Log Workout - {day}")
    popup.geometry("400x450")

    popup_title = ctk.CTkLabel(
        popup,
        text=f"Log Workout for {day}",
        font=("Arial", 20)
    )
    popup_title.pack(pady=20)

    completed_label = ctk.CTkLabel(
        popup,
        text="Did you complete this workout?"
    )
    completed_label.pack(pady=(10, 5))

    completed_menu = ctk.CTkOptionMenu(
        popup,
        values=["yes", "no"],
        width=200
    )
    completed_menu.pack(pady=5)

    distance_label = ctk.CTkLabel(
        popup,
        text="Actual distance run (miles):"
    )
    distance_label.pack(pady=(10, 5))

    distance_entry = ctk.CTkEntry(popup, width=200)
    distance_entry.pack(pady=5)

    pace_label = ctk.CTkLabel(
        popup,
        text="Actual average pace (minutes per mile):"
    )
    pace_label.pack(pady=(10, 5))

    pace_entry = ctk.CTkEntry(popup, width=200)
    pace_entry.pack(pady=5)

    error_label = ctk.CTkLabel(
        popup,
        text="",
        text_color="red"
    )
    error_label.pack(pady=10)

    def save_workout():
        completed_value = completed_menu.get()

        if completed_value == "no":
            log_workout(day, False, 0.0, None)
            popup.destroy()
            return

        try:
            actual_distance = float(distance_entry.get())
            actual_pace = float(pace_entry.get())

            log_workout(day, True, actual_distance, actual_pace)
            popup.destroy()

        except ValueError:
            error_label.configure(
                text="Please enter valid numbers for distance and pace."
            )

    save_button = ctk.CTkButton(
        popup,
        text="Save Workout",
        command=save_workout
    )
    save_button.pack(pady=15)

# Start on screen 1.
show_screen1()

# Run the app
app.mainloop()
