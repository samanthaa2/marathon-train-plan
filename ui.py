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

    
