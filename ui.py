import customtkinter as ctk

# Set the appearance and color theme of the app.
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main app window.
app = ctk.CTk()
app.title("Marathon Training Plan Generator")
app.geometry("700x500")


# This function runs when the button is clicked.
# It gets the text from the entry box and displays it in the output box.
def button_clicked():
    weekly_mileage = weekly_mileage_entry.get()

    output_box.delete("1.0", "end")
    output_box.insert("1.0", f"You entered: {weekly_mileage} miles per week")


# Title label
title_label = ctk.CTkLabel(
    app,
    text="Marathon Training Plan Generator",
    font=("Arial", 24)
)
title_label.pack(pady=20)

# Label for the input field
weekly_mileage_label = ctk.CTkLabel(
    app,
    text="How many miles are you currently running per week?"
)
weekly_mileage_label.pack(pady=(10, 5))

# Entry box for the input
weekly_mileage_entry = ctk.CTkEntry(
    app,
    width=200
)
weekly_mileage_entry.pack(pady=5)

# Button
generate_button = ctk.CTkButton(
    app,
    text="Submit",
    command=button_clicked
)
generate_button.pack(pady=15)

# Output textbox
output_box = ctk.CTkTextbox(
    app,
    width=500,
    height=200
)
output_box.pack(pady=20)

# Start the app
app.mainloop()
