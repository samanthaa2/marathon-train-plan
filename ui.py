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


# This function collects all user inputs from the interface.
def collect_runner_info():
    runner_info = {
        "weekly_mileage": weekly_mileage_entry.get(),
        "longest_run": longest_run_entry.get(),
        "average_pace": average_pace_entry.get(),
        "running_days": running_days_entry.get(),
        "goal": goal_menu.get()
    }
    return runner_info


# This function runs when the button is clicked.
# It collects the inputs and displays them in the output box.
def button_clicked():
    runner_info = collect_runner_info()

    output_box.delete("1.0", "end")
    output_box.insert("1.0", f"Collected runner info:\n{runner_info}")


# Title label
title_label = ctk.CTkLabel(
    app,
    text="Marathon Training Plan Generator",
    font=("Arial", 24)
)
title_label.pack(pady=20)


# Weekly mileage input
weekly_mileage_label = ctk.CTkLabel(
    app,
    text="How many miles are you currently running per week?"
)
weekly_mileage_label.pack(pady=(10, 5))

weekly_mileage_entry = ctk.CTkEntry(app, width=250)
weekly_mileage_entry.pack(pady=5)


# Longest run input
longest_run_label = ctk.CTkLabel(
    app,
    text="What is your longest recent run (in miles)?"
)
longest_run_label.pack(pady=(10, 5))

longest_run_entry = ctk.CTkEntry(app, width=250)
longest_run_entry.pack(pady=5)


# Average pace input
average_pace_label = ctk.CTkLabel(
    app,
    text="What is your average pace in minutes per mile?"
)
average_pace_label.pack(pady=(10, 5))

average_pace_entry = ctk.CTkEntry(app, width=250)
average_pace_entry.pack(pady=5)


# Running days input
running_days_label = ctk.CTkLabel(
    app,
    text="How many days per week can you run?"
)
running_days_label.pack(pady=(10, 5))

running_days_entry = ctk.CTkEntry(app, width=250)
running_days_entry.pack(pady=5)


# Goal dropdown
goal_label = ctk.CTkLabel(
    app,
    text="What is your goal?"
)
goal_label.pack(pady=(10, 5))

goal_menu = ctk.CTkOptionMenu(
    app,
    values=["finish", "improve time"],
    width=250
)
goal_menu.pack(pady=5)


# Submit button
submit_button = ctk.CTkButton(
    app,
    text="Submit",
    command=button_clicked
)
submit_button.pack(pady=20)


# Output textbox
output_box = ctk.CTkTextbox(
    app,
    width=600,
    height=180
)
output_box.pack(pady=20)


# Start the app
app.mainloop()
