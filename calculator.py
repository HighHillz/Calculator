# In progress: Polishing history UI

import customtkinter as ctk
import math

# Global variable to store the equation string
result_text = "0"

# Functions to manipulate the equation string

def log_history():
    """Log a new calculation in the history frame."""
    index = len(prev_calc) - 1  # Last added calculation index

    # Create a frame for this history entry
    history_entry = ctk.CTkFrame(
        history_frame,
        corner_radius=10,
        fg_color="#2c2c2c",
        width=280,
        height=50,
        cursor="hand2"
    )
    history_entry.grid(row=index + 1, column=0, padx=10, pady=5, sticky="ew")  # index+1 because title is row=0
    prev_calc_frames[index] = history_entry

    # Left: Equation
    eq_label = ctk.CTkLabel(
        history_entry,
        text=prev_calc[index][0],
        font=("Consolas", 12),
        text_color="#CCCCCC",
        anchor="w",
        justify="left"
    )
    eq_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # Right: Result
    result_label = ctk.CTkLabel(
        history_entry,
        text=prev_calc[index][1],
        font=("Consolas", 12),
        text_color="#00FF99",
        anchor="e",
        justify="right"
    )
    result_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    # Make 2 columns expand properly
    history_entry.grid_columnconfigure(0, weight=3)
    history_entry.grid_columnconfigure(1, weight=2)

    # Optional: clicking the frame loads the previous calculation
    history_entry.bind("<Button-1>", lambda e, data=prev_calc[index]: get_prev_calc(data))
    eq_label.bind("<Button-1>", lambda e, data=prev_calc[index]: get_prev_calc(data))
    result_label.bind("<Button-1>", lambda e, data=prev_calc[index]: get_prev_calc(data))


def close_const(const_window, window):
    """Close constants window and re-enable the main window."""
    const_window.destroy()  # Close the constants window
    window.attributes("-disabled", False)  # Re-enable the main window
    window.attributes("-topmost", True)  # Re-open the main window on top

def open_const():
    """Open a window containing various constants to be added to the equation."""
    global result_text
    const_window = ctk.CTkToplevel(window)  # Create a new popup window
    const_window.title("Constants")
    const_window.geometry("200x200")
    const_window.resizable(0, 0)
    const_window.attributes("-topmost", True)  # Keep the window on top
    window.attributes("-disabled", True)  # Disable the main window
    const_window.protocol("WM_DELETE_WINDOW", lambda: close_const(const_window, window))

    # Define the layout for the constant buttons
    const_layout = [
        ["π", "e"]
    ]

    # Const Button Layout
    layout_frame = ctk.CTkFrame(const_window)
    layout_frame.pack(pady=20)

    # Create Const Buttons
    for i, row in enumerate(const_layout):
        for j, unit in enumerate(row):
            btn_bg = special_bg.get(unit, default_bg)
            ctk.CTkButton(
                layout_frame,
                text=unit,
                width=80,
                height=30,
                cursor="hand2",
                fg_color=btn_bg,
                text_color="#FFFFFF",
                font=button_font,
                command=lambda m=unit: write_equation(m)
            ).grid(row=i, column=j, padx=5, pady=5)

def format_function(item):
    """Format the input item to be added to the equation string."""
    global result_text, res_fetched

    # Handle special cases for input formatting
    if item == "x^a":  # Replace "x^a" with "^" for exponentiation
        result_text += "^"
    elif item in ["ln", "sin", "cos", "tan"]:  # Add ln/sin/cos/tan formatting
        result_text = f"{item}({result_text})"
    elif item == "|x|":  # Toggle absolute value formatting
        result_text = f"|{result_text}|"
    elif item == "%":  # Convert percentage to division by 100
        result_text += "/100"
    elif item == "Const":  # Add constant "e" to the equation
        open_const()
    else:
        # Reset result_text if it is "0", otherwise append the item

        result_text = "" if result_text == "0" else result_text

        if item.isdigit() and res_fetched:
            result_text = ""

        result_text += item
    res_fetched = False

def to_abs(exp):
    """Convert the expression to absolute value."""
    # Count the number of absolute value pairs (|x|)
    num_mod = exp.count("|") // 2
    mod_counted = 0
    while num_mod > 0:
        sub_exp = ""
        for i in exp:
            if mod_counted == num_mod:
                if i != "|":
                    sub_exp += i
                else:
                    # Replace "|x|" with "abs(x)"
                    exp = exp.replace(f"|{sub_exp}|", f"math.fabs({sub_exp})")
                    num_mod -= 1
                    mod_counted = 0
                    break
            if i == "|":
                mod_counted += 1
    return exp

def write_equation(item):
    """Write the equation to the result screen."""
    global result_text, res_fetched

    if res_fetched:
        posted_eq.configure(text="")

    if item == "C":  # Clear the equation
        result_text = "0"
    elif item == "Back":  # Remove the last character
        result_text = result_text[:-1] if len(result_text) > 1 else "0"
    elif item == "=":  # Evaluate the equation
        try:
            # Write equation to be computed on top of the screen
            posted_eq.configure(text=result_text + " =")

            # Replace symbols for evaluation and handle absolute values
            expression = result_text.replace("×", "*").replace("÷", "/").replace("^", "**").replace("ln", "math.log").replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan").replace("e", str(math.e)).replace("π", str(math.pi))

            expression = to_abs(expression) #Convert to absolute value
            result_text = str(eval(expression, {"math": math, "__builtins__": {}})) # Evaluate the expression
            prev_calc[len(prev_calc)] = [posted_eq.cget("text"), result_text]  # Store the equation and result in history
            log_history()

            res_fetched = True  # Set flag to indicate result is fetched
        except:
            result_text = "Error"
    else:
        format_function(item)
    equation.configure(text=result_text)

def get_prev_calc(prev_calc_set):
    """Get the previous calculation as per trigger."""
    
    global result_text, res_fetched

    result_text = prev_calc_set[1]
    equation.configure(text=result_text)  # Update the equation label
    posted_eq.configure(text=prev_calc_set[0])  # Update the posted equation label

    res_fetched = True # Result has been fetched as previous calculation has been used

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Calculator")
window.geometry("700x375")
window.resizable(0, 0)

# Calculator frame
calc_frame = ctk.CTkFrame(window, corner_radius=0)
calc_frame.grid(column=0, row=0, sticky="nsew")

# History frame
history_frame = ctk.CTkScrollableFrame(window,corner_radius=0)
history_frame.grid(column=1, row=0, sticky="nsew")
window.grid_columnconfigure(1, weight=1)

title_label = ctk.CTkLabel(
    history_frame,
    text="History",
    font=("Consolas", 14),
    justify="center",
    text_color="#777777"
)
title_label.grid(row=0, column=0, columnspan=2, pady=10, padx = 10)

# Storing previous calculations
prev_calc = {}
prev_calc_frames = {}

# Equation Screen
equation_frame = ctk.CTkFrame(calc_frame, corner_radius=0)
equation_frame.pack(pady=0, fill="x")

# Label to display the equation to be computed
posted_eq = ctk.CTkLabel(
    equation_frame,
    text="",
    font=("Consolas", 14),
    text_color="#AAAAAA",
    anchor="e",
    justify="right"
)
posted_eq.pack(fill="both", padx=10, pady=0)

# Result Screen
result_frame = ctk.CTkFrame(calc_frame, corner_radius=0)
result_frame.pack(pady=0, fill="x")

res_fetched = False # Flag to check if result is fetched

# Label to display the equation/result
equation = ctk.CTkLabel(
    result_frame,
    text="0",
    font=("Consolas", 24),
    text_color="#FFFFFF",
    anchor="e",
    justify="right"
)
equation.pack(fill="both", padx=10, pady=0)

# Button Layout
layout_frame = ctk.CTkFrame(calc_frame, corner_radius=0)
layout_frame.pack(pady=20)

# Define the layout of the calculator buttons
layout = [
    ["Const", "x^a", "ln", "C"],
    ["sin", "cos", "tan", "Back"],
    ["(", ")", "|x|", "+"],
    ["1", "2", "3", "-"],
    ["4", "5", "6", "×"],
    ["7", "8", "9", "÷"],
    [".", "0", "%", "="]
]

# Simplified Colour Setup
button_font = ("Consolas", 14, "bold")
default_bg = "#3a3a3a"  # Default button background color
active_bg = "#505050"  # Button background color when active
special_bg = {
    "=": "#2ecc71",  # Green for "=" button
    "C": "#e74c3c",  # Red for "C" button
    "Back": "#e74c3c"  # Red for "Back" button
}

# Create Buttons
for i, row in enumerate(layout):
    for j, unit in enumerate(row):
        btn_bg = special_bg.get(unit, default_bg)  # Use special color if defined
        ctk.CTkButton(
            layout_frame,
            text=unit,
            width=80,
            height=30,
            cursor="hand2",
            fg_color=btn_bg,
            text_color="#FFFFFF",
            font=button_font,
            command=lambda m=unit: write_equation(m)  # Bind button to write_equation
        ).grid(row=i, column=j, padx=5, pady=5)

# Run the application
window.mainloop()
