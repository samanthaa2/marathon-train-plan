# marathon-train-plan

## Project Overview
For my final project, I created a marathon training planner that builds a personalized training schedule and then adjusts it based on the user’s progress. The idea came from one of my dream goals, which is to run a marathon.

This program asks the user for information like their current weekly mileage, longest recent run, average pace, running availability, weeks until race day, goal, preferred long run day, and any required off days. Based on that information, it generates a baseline week of marathon training with easy runs, long runs, rest days, and workout days when appropriate.

The program also allows the user to log completed workouts and generate the next week of training using updated information from the previous week. After each run, the user can enter workout data such as actual distance and actual average pace, and the planner uses that information to update future weeks.

## Current Features
- Collects runner information through a multi-step graphical user interface
- Generates a baseline week of marathon training
- Assigns run types such as easy run, long run, workout, and rest
- Uses the runner’s current mileage, pace, and schedule constraints to shape the plan
- Allows the user to specify required off days and a preferred long run day
- Supports both a finish goal and an improve-time goal
- Lets the user log completed workouts from the generated plan
- Generates future training weeks using updated workout data from the previous week

## Files
- `ui.py` - runs the graphical user interface for the project
- `generator.py` - contains the logic for generating each training week
- `updater.py` - updates runner information based on logged workouts from the previous week
- `runner_info.py` - contains the original terminal-based runner input functions
- `README.md` - explains the project and how to run it

## How to Run the Project
This project is currently designed to be run locally on your computer, not in a browser-only or headless environment.

### 1. Make sure Python is installed
You need Python 3 installed on your computer.

### 2. Install the required package
This project uses `customtkinter` for the graphical user interface. In Terminal, run:

``bash
python3 -m pip install customtkinter``
### 3. Open the project folder

In Terminal, change into the project folder:

``bash
cd path/to/marathon-train-plan``

### 4. Run the User Interface
To launch the app, run:
''bash
python3 ui.py''

## Important Setup Notes
- The graphical interface uses `CustomTkinter`, so the project should be run locally on a machine with a display. For example, if on a mac you can run it on the built in python terminal.
- Running the GUI in a headless browser-based environment may cause display errors.
- I tested the GUI locally on my computer (a mac) using Python and CustomTkinter.

## How to Use the Program
1. Run `ui.py`
2. Enter your current training information
3. Enter your schedule and race information
4. Enter any required off days if needed
5. Select your training goal
6. Generate your baseline week 1 training plan
7. View the generated schedule in the app
8. Click on workout buttons to log completed runs
9. Generate the next week of training based on the updated workout data

## If I Had More Time I Would:
Have more information input with the workout data and used to update following week run plans. While this is quite simple to implement in code, I wasn't sure how factors like perceived effort needed to be interpretted in suggested workouts, and unfortunately did not have the time to research it. I would also have added a summary screen at the end (like maybe number of runs completed, total miles run, words of encouragement, etc.).

## External Contributors / Sources
I used ChatGPT to help organize code, debug logic, and understand how to build a graphical user interface with CustomTkinter. I reviewed, edited, and tested the code myself.

I also used the official CustomTkinter documentation as a reference while learning how to build the GUI:

https://customtkinter.tomschimansky.com/

If I incorporate any additional outside code, tutorials, or examples later, I will add them here.
