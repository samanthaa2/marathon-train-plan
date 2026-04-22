import customtkinter as ctk
# import/connect the ui to our plan generator
from generator import generate_baseline_week
# Set the appearance and color theme of the app.
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main app window.
app = ctk.CTk()
app.title("Marathon Training Plan Generator")
app.geometry("800x650")

# create the runner dictionary to store the runner data
runner_info = {}

# create a function to hide all frames so only one screen is visible at a time
def hide_all_frames():
    screen1_frame.pack_forget()
    screen2_frame.pack_forget()
    results_frame.pack_forget()

# create a function that shows the first screen
def show_screen1():
    hide_all_frames()
    screen1_frame.pack(fill = 'both', expand = True, padx = 20, pady = 20)

# function to how second screen
def show_screen2():
    hide_all_frames()
    screen2_frame.pack(fill = 'both', expand = True, padx = 20, pady = 20)


# function to show results
def show_results():
    hide_all_frames()
    results_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Function to save data from screen 1 and move to screen 2;
# called when next button on screen 1 is pressed
def go_to_screen2():
    try:
        runner_info["weekly_mileage"] = float(weekly_mileage_entry.get())
        runner_info["longest_run"] = float(longest_run_entry.get())
        runner_info["average_pace"] = float(average_pace_entry.get())

        show_screen2()
    except ValueError:
        screen1_error_label.configure(
            text = 'Please enate valid numbers for all fields.'
        )

# This function saves the data from screen 2, generates the plan,
# and shows the result screen.
def generate_plan():
    try:
        runner_info["running_days"] = int(running_days_entry.get())
        runner_info["weeks_until_race"] = int(weeks_until_race_entry.get())
        runner_info["goal"] = goal_menu.get()
        runner_info["long_run_day"] = long_run_day_menu.get()

        # For now, we are hard-coding these values until we build later screens.
        runner_info["time_goal"] = None
        runner_info["off_days"] = []

        baseline_week = generate_baseline_week(runner_info)

        # Clear the old output before inserting the new plan.
        results_box.delete("1.0", "end")

        # Show the runner info first.
        results_box.insert("end", "Runner Information:\n")
        results_box.insert("end", f"{runner_info}\n\n")

        # Show the generated plan.
        results_box.insert("end", "Week 1 Plan:\n")
        for day, workout in baseline_week.items():
            results_box.insert("end", f"{day}: {workout}\n")

        show_results()

    except ValueError:
        screen2_error_label.configure(
            text="Please enter valid values before generating the plan."
        )


### INITIALIZE SCREEN 1: BASIC TRAINING BACKGROUND
screen1_frame = ctk.CTkFrame(app)

screen1_title = ctk.CTkLabel(screen1_frame, text = "Step 1: Current Training", font = ("Arial", 24))
screen1_title.pack(pady=20)

weekly_mileage_label = ctk.CTkLabel(screen1_frame, text = "How many miles are you currently running per week?")
weekly_mileage_label.pack(pady = (10,5))

weekly_mileage_entry = ctk.CTkEntry(screen1_frame, width = 250)
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

### SCREEN 2: SCHEDULE AND RACE INFO
screen2_frame = ctk.CTkFrame(app)

screen2_title = ctk.CTkLabel(
    screen2_frame,
    text="Step 2: Race and Schedule",
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

goal_label = ctk.CTkLabel(
    screen2_frame,
    text="What is your goal?"
)
goal_label.pack(pady=(10, 5))

goal_menu = ctk.CTkOptionMenu(
    screen2_frame,
    values=["finish", "improve time"],
    width=250
)
goal_menu.pack(pady=5)

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

screen2_generate_button = ctk.CTkButton(
    screen2_frame,
    text="Generate Week 1 Plan",
    command=generate_plan
)
screen2_generate_button.pack(pady=10)

### RESULTS SCREEN-- PRINT WEEK 1 PLAN
results_frame = ctk.CTkFrame(app)

results_title = ctk.CTkLabel(
    results_frame,
    text="Your Week 1 Plan",
    font=("Arial", 24)
)
results_title.pack(pady=20)

results_box = ctk.CTkTextbox(
    results_frame,
    width=650,
    height=320
)
results_box.pack(pady=20)

results_back_button = ctk.CTkButton(
    results_frame,
    text="Back to Step 1",
    command=show_screen1
)
results_back_button.pack(pady=10)


# Start by showing the first screen.
show_screen1()

# Start the app.
app.mainloop()
