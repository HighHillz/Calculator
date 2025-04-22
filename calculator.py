import tkinter as tk
import math

# Global variable to store the equation string
result_text = "0"

# Functions to manipulate the equation string

def close_const(const_window, window):
    """Close constants window and re-enable the main window."""
    const_window.destroy()  # Close the constants window
    window.attributes("-disabled", False)  # Re-enable the main window
    window.attributes("-topmost", True)  # Re-open the main window on top

def open_const():
    """Open a window containing various constants to be added to the equation."""
    global result_text
    const_window = tk.Toplevel(window)  # Create a new popup window
    const_window.title("Constants")
    const_window.geometry("200x200")
    const_window.configure(bg="#1e1e1e")
    const_window.resizable(0, 0)
    const_window.attributes("-topmost", True)  # Keep the window on top
    window.attributes("-disabled", True) # Disable the main window
    const_window.protocol("WM_DELETE_WINDOW", lambda: close_const(const_window, window))

    # Define the layout for the constant buttons
    const_layout = [
        ["π", "e"]
    ]

    # Const Button Layout
    layout_frame = tk.Frame(const_window, bg="#1e1e1e")
    layout_frame.pack(pady=20)

    # Create Const Buttons
    for i, row in enumerate(const_layout):
        for j, unit in enumerate(row):
            btn_bg = special_bg.get(unit, default_bg)
            tk.Button(
                layout_frame,
                text=unit,
                width=8,
                height=1,
                cursor="hand2",
                bg=btn_bg,
                fg="#FFFFFF",
                font=button_font,
                activebackground=active_bg,
                activeforeground="#FFFFFF",
                command=lambda m=unit: write_equation(m)
            ).grid(row=i, column=j, padx=5, pady=5)

def format_function(item):
    """Format the input item to be added to the equation string."""
    global result_text

    # Handle special cases for input formatting
    if item == "x^a":  # Replace "x^a" with "^" for exponentiation
        result_text += "^"
    elif item in ["ln","sin","cos","tan"]:  # Add ln/sin/cos/tan formatting
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
        result_text += item

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
                    exp = exp.replace(f"|{sub_exp}|", f"abs({sub_exp})")
                    num_mod -= 1
                    mod_counted = 0
                    break
            if i == "|":
                mod_counted += 1
    return exp

def write_equation(item):
    """Write the equation to the result screen."""
    global result_text

    if item == "C":  # Clear the equation
        result_text = "0"
    elif item == "Back":  # Remove the last character
        result_text = result_text[:-1] if len(result_text) > 1 else "0"
    elif item == "=":  # Evaluate the equation
        try:
            # Replace symbols for evaluation and handle absolute values
            expression = result_text.replace("×", "*").replace("÷", "/").replace("^", "**").replace("ln", "math.log").replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan").replace("e", str(math.e)).replace("π", str(math.pi))
            
            expression = to_abs(expression)
            result_text = str(eval(expression))  # Evaluate the expression
        except:
            result_text = "Error"
    else:
        format_function(item)
    equation.config(text=result_text)

# GUI Setup
window = tk.Tk()
window.title("Calculator")
window.geometry("400x500")
window.configure(bg="#1e1e1e")
window.resizable(0, 0)

# Result Screen
result_frame = tk.Frame(window, bg="#1e1e1e")
result_frame.pack(pady=20, fill="x")

# Label to display the equation/result
equation = tk.Label(
    result_frame,
    text="0",
    font=("Consolas", 24),
    bg="#1e1e1e",
    fg="#FFFFFF",
    justify="right",
    anchor="e"
)
equation.pack(fill="both", padx=10, pady=10)

# Button Layout
layout_frame = tk.Frame(window, bg="#1e1e1e")
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
        tk.Button(
            layout_frame,
            text=unit,
            width=8,
            height=1,
            cursor="hand2",
            bg=btn_bg,
            fg="#FFFFFF",
            font=button_font,
            activebackground=active_bg,
            activeforeground="#FFFFFF",
            command=lambda m=unit: write_equation(m)  # Bind button to write_equation
        ).grid(row=i, column=j, padx=5, pady=5)

# Run the application
window.mainloop()
