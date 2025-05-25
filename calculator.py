import customtkinter as ctk
import math

class Calculator:
    mult, div, pi = "×", "÷", "π"

    def __init__(self, frame, window, disabled_keys = []):
        self.result_text = "0"
        self.res_fetched = False
        self.frame = frame
        self.const_window = None
        self.window = window
        self.disabled_keys = disabled_keys

        self.layout = {
            "main": [
                ["Const", "x^a", "ln", "C"],
                ["sin", "cos", "tan", "Back"],
                ["(", ")", "|x|", "+"],
                ["1", "2", "3", "-"],
                ["4", "5", "6", Calculator.mult],
                ["7", "8", "9", Calculator.div],
                [".", "0", "%", "="]
            ],
            "constants": [["e", Calculator.pi]]
        }
        self.button_font = ("Consolas", 14, "bold")
        self.default_bg = "#3a3a3a"
        self.disabled_bg = "#111111"
        self.special_bg = {"=": "#2ecc71", "C": "#e74c3c", "Back": "#e74c3c"}

    def build_result_frame(self):
        for font, var, color in [
            (("Consolas", 14), "posted_eq", "#AAAAAA"),
            (("Consolas", 24), "equation", "#FFFFFF")
        ]:
            frame = ctk.CTkFrame(self.frame, corner_radius=0)
            frame.pack(pady=0, fill="x")
            label = ctk.CTkLabel(
                frame, text="", font=font, text_color=color,
                anchor="e", justify="right"
            )
            label.pack(fill="both", padx=10, pady=0)
            setattr(self, var, label)
        self.equation.configure(text="0")

    def build_layout(self):
        layout_frame = ctk.CTkFrame(self.frame, corner_radius=0)
        layout_frame.pack(pady=0)
        for i, row in enumerate(self.layout["main"]):
            for j, unit in enumerate(row):
                ctk.CTkButton(
                    layout_frame, text=unit, width=80, height=35,
                    cursor="hand2", fg_color=self.disabled_bg if unit in self.disabled_keys else self.special_bg.get(unit, self.default_bg),
                    text_color="#FFF", font=self.button_font, text_color_disabled=self.disabled_bg,
                    state="disabled" if unit in self.disabled_keys else "normal",
                    command=lambda m=unit: self.write_equation(m)
                ).grid(row=i, column=j, padx=5, pady=5)

    def buildCalculator(self):
        self.build_result_frame()
        self.build_layout()

    def write_equation(self, item):
        if self.res_fetched:
            self.posted_eq.configure(text="")
            self.result_text = "0"
        if item == "C":
            self.result_text = "0"
        elif item == "Back":
            self.result_text = self.result_text[:-1] if len(self.result_text) > 1 else "0"
        elif item == "Const":
            self.open_const()
        elif item == "=":
            try:
                self.posted_eq.configure(text=self.result_text + " =")
                expr = self.result_text.replace(self.mult, "*").replace(self.div, "/") \
                    .replace("^", "**").replace("ln", "math.log") \
                    .replace("sin", "math.sin").replace("cos", "math.cos") \
                    .replace("tan", "math.tan").replace("e", str(math.e)) \
                    .replace(self.pi, str(math.pi))
                expr = self.to_abs(expr)
                self.result_text = str(eval(expr, {"math": math, "__builtins__": {}}))
                self.doSomething() #A function that can be used to do what is intended (hook function)
            except:
                self.result_text = "Error"
            self.res_fetched = True
        else:
            self.format_function(item)
        self.equation.configure(text=self.result_text)

    def format_function(self, item):
        if item == "x^a":
            self.result_text += "^"
        elif item in ["ln", "sin", "cos", "tan"]:
            self.result_text = f"{item}({self.result_text})"
        elif item == "|x|":
            self.result_text = f"|{self.result_text}|"
        elif item == "%":
            self.result_text += "/100"
        else:
            if self.result_text == "0" or (item.isdigit() and self.res_fetched):
                self.result_text = ""
            if any(item in row for row in self.layout["constants"]):
                self.close_const(self.const_window, self.window)
            self.result_text += item
        self.res_fetched = False

    def to_abs(self, exp):
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

    def open_const(self):
        self.const_window = ctk.CTkToplevel(self.window)
        self.const_window.title("Constants")
        self.const_window.geometry("200x200")
        self.const_window.resizable(0, 0)
        self.const_window.attributes("-topmost", True)
        self.window.attributes("-disabled", True)
        self.const_window.protocol("WM_DELETE_WINDOW", lambda: self.close_const(self.const_window, self.window))
        layout_frame = ctk.CTkFrame(self.const_window)
        layout_frame.pack(pady=20)
        for i, row in enumerate(self.layout["constants"]):
            for j, unit in enumerate(row):
                ctk.CTkButton(
                    layout_frame, text=unit, width=80, height=30,
                    cursor="hand2", fg_color=self.special_bg.get(unit, self.default_bg),
                    text_color="#FFF", font=self.button_font,
                    command=lambda m=unit: self.write_equation(m)
                ).grid(row=i, column=j, padx=5, pady=5)

    def close_const(self, const_window, main_window):
        const_window.destroy()
        main_window.attributes("-disabled", False)
        main_window.focus_force()

    def doSomething(self): #Nothing happens without using this class somewhere
        pass