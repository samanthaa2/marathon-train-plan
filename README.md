# marathon-train-plan

## Project Overview
For my final project, I created a marathon training planner that builds a personalized training schedule and then adjusts it based on the user’s progress. The idea came from one of my dream goals, which is to run a marathon.

This program asks the user for information like their current weekly mileage, longest recent run, average pace, running availability, weeks until race day, goal, preferred long run day, and any required off days. Based on that information, it generates a baseline week of marathon training with easy runs, long runs, rest days, and workout days when appropriate.

The long-term goal of the project is for the planner to update over time based on the user’s completed workouts. After each run, the user will be able to enter workout stats such as distance, time, and effort level, and the program will use that information to adjust future training weeks.

## Current Features
- Collects runner information through a multi-step graphical user interface
- Generates a baseline week of marathon training
- Assigns run types such as easy run, long run, workout, and rest
- Uses the runner’s current mileage, pace, and schedule constraints to shape the plan
- Allows the user to specify required off days and a preferred long run day
- Supports both a finish goal and an improve-time goal

## Files
- `ui.py` - runs the graphical user interface for the project
- `generator.py` - contains the logic for generating the baseline training week
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

## Future Plans
The next stage of the project is to let the user log completed workouts and use that data to adjust future weeks of training. The program will eventually take into account workout completion, actual distance, actual time, and effort level in order to make the training plan more adaptive.

## External Contributors / Sources
I used ChatGPT to help organize code, debug logic, and understand how to build a graphical user interface with CustomTkinter. I reviewed, edited, and tested the code myself.

I also used the official CustomTkinter documentation as a reference while learning how to build the GUI:

https://customtkinter.tomschimansky.com/

If I incorporate any additional outside code, tutorials, or examples later, I will add them here.
