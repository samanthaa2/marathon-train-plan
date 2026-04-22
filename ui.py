# A file that creates the user interface for this project!!!

# import customTkinter, which is how we will be constructing this user interface
import customtkinter as ctk

# set overall appearance of the app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create maun app window
app = ctk.CTk()
app.title("Marathon Training Plan Generator")
app.geometry("700x500")

def button_clicked():
    output_box.delete("1.0", "end")
    output_box.insert("1.0", "Hello! Your training plab will appear here.")

# Create a title label at the top of the window
title_label = ctk.CTkLabel(app, text = "Marathon Training Plan Generator", font = ("Arial", 24))

# create a button for the user to click
generate_button = ctk. CTkButton(app, text = "Generate Plan", command = button_clicked)
generate_button.pack(pady = 10)

# create a text box where the output will be displayed
output_box = ctk.CTkTextBox(app, width = 500, height = 250)
output_box.pack(pady = 20)

# start the app
app.mainloop()
