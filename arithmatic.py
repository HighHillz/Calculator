### BASIC CALCULATOR ###


## IMPORTS ##
import customtkinter as ctk
import math
from calculator import Calculator

class History(Calculator):
    # Storing previous calculations
    prev_calc = {}
    prev_calc_frames = {}
    
    def __init__(self, calc_frame, history_frame, window, disabled_keys = []):
        super().__init__(calc_frame, window, disabled_keys)
        self.history_frame = history_frame
    
    def doSomething(self):
        History.prev_calc[len(History.prev_calc)] = [self.posted_eq.cget("text"), self.result_text]  # Store the equation and result in history
        self.log_history()

    def log_history(self):
        index = len(History.prev_calc) - 1  # Last added calculation index

        # Create a frame for this history entry
        history_entry = ctk.CTkFrame(
            self.history_frame,
            corner_radius=10,
            fg_color="#2c2c2c",
            width=280,
            height=50,
            cursor="hand2"
        )
        history_entry.grid(row=index + 1, column=0, padx=10, pady=5, sticky="ew")  # index+1 because title is row=0
        History.prev_calc_frames[index] = history_entry

        # Left: Equation
        eq_label = ctk.CTkLabel(
            history_entry,
            text=History.prev_calc[index][0],
            font=("Consolas", 12),
            text_color="#CCCCCC",
            anchor="w",
            justify="left"
        )
        eq_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Right: Result
        result_label = ctk.CTkLabel(
            history_entry,
            text=History.prev_calc[index][1],
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
        history_entry.bind("<Button-1>", lambda e, data=History.prev_calc[index]: self.get_prev_calc(data))
        eq_label.bind("<Button-1>", lambda e, data=History.prev_calc[index]: self.get_prev_calc(data))
        result_label.bind("<Button-1>", lambda e, data=History.prev_calc[index]: self.get_prev_calc(data))

    def get_prev_calc(self, prev_calc_set):
        global result_text, res_fetched

        result_text = prev_calc_set[1]
        self.equation.configure(text=result_text)  # Update the equation label
        self.posted_eq.configure(text=prev_calc_set[0])  # Update the posted equation label

        self.res_fetched = True # Result has been fetched as previous calculation has been used

# GUI Setup
def run(window):
    for widget in window.winfo_children():
        widget.destroy()
        
    window.title("Arithmatic Calculator")
        
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
        
    History(calc_frame, history_frame, window).buildCalculator()
