import customtkinter as ctk
import random
from calculator import Calculator

class Game(Calculator):
    bot_name = "SigmaBot"

    def __init__(self, calc_frame, chat_frame, window, disabled_keys=[]):
        super().__init__(calc_frame, window, disabled_keys)
        self.chat_box = ctk.CTkTextbox(
            chat_frame, width=325, font=("Consolas", 13),
            text_color="#FFF", fg_color="#2c2c2c",
            corner_radius=10, wrap="word", state="disabled"
        )
        self.chat_box.grid(row=1, column=0, pady=10, padx=5, sticky="nsew")
        chat_frame.grid_rowconfigure(1, weight=1)
        self.window = window
        self.player_score = self.bot_score = 0
        self.sender = ""

    def say(self, sender, message):
        self.chat_box.configure(state="normal")
        prefix = f"\n{sender.upper()}:\n" if sender != self.sender else ""
        self.chat_box.insert("end", f"{prefix}{message}\n")
        self.chat_box.configure(state="disabled")
        self.sender = sender
        self.chat_box.see("end")
        
    def show_scores(self):
        score_frame = ctk.CTkFrame(self.window, fg_color="black", width=50, height=10)
        score_frame.place(x=520, y=5)
        ctk.CTkLabel(score_frame, text="You", width=75, height=4, text_color="white", font=('Consolas', 12)).grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(score_frame, text=self.player_score, width=75, height=4, text_color="#2ecc71", font=('Consolas', 16, 'bold')).grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(score_frame, text=Game.bot_name, width=75, height=4, text_color="white", font=('Consolas', 12)).grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkLabel(score_frame, text=self.bot_score, width=75, height=4, text_color="#e74c3c", font=('Consolas', 16, 'bold')).grid(row=2, column=2, padx=5, pady=5)

class NumberGuessing(Game):
    def __init__(self, calc_frame, chat_frame, window, disabled_keys=[]):
        super().__init__(calc_frame, chat_frame, window, disabled_keys)
        self.gameOver = False
        self.chances = 7
        self.number_range = {"min": 1, "max": 100}
        self.target_number = random.randint(self.number_range["min"], self.number_range["max"])
        self.say(self.bot_name, f"Welcome to Guess the Number! I picked a number between {self.number_range['min']} and {self.number_range['max']}. Guess it in {self.chances} chances!")
        self.get_turns()
        self.show_scores()

    def get_turns(self):
        self.say(self.bot_name, f"{self.chances} chances left. Enter your guess!")

    def play_game(self, guess):
        try:
            guess = int(guess)
            if self.gameOver:
                self.reset_game()
            else:
                if not (self.number_range["min"] <= guess and guess <= self.number_range["max"]):
                    self.say(self.bot_name, f"Enter a number between {self.number_range['min']} and {self.number_range['max']}.")
                elif guess == self.target_number:
                    self.player_score += 1
                    self.say(self.bot_name, f"Congrats! You guessed it! The number was {self.target_number}.")
                    self.show_scores()
                    self.gameOver = True
                    self.say(self.bot_name, f"If you want to play again, enter any number.")
                else:
                    self.chances -= 1
                    if self.chances == 0:
                        self.bot_score += 1
                        self.say(self.bot_name, f"Out of chances! The number was {self.target_number}.")
                        self.show_scores()
                        self.gameOver = True
                        self.say(self.bot_name, f"If you want to play again, enter any number.")
                    else:
                        hint = "low" if guess < self.target_number else "high"
                        self.say(self.bot_name, f"Your guess was {hint}! Try again.")
                        self.get_turns()
        except Exception:
            self.say(self.bot_name, "Enter a valid number.")
    
    def reset_game(self):
        self.gameOver = False
        self.chances = 7
        self.target_number = random.randint(self.number_range["min"], self.number_range["max"])

        self.say(self.bot_name, f"Sure! I have picked a new number. Try to guess it within {self.chances} chances.")

    def doSomething(self):
        self.say("You", self.result_text)
        self.play_game(self.result_text)

def run(window):
    for w in window.winfo_children():
        w.destroy()
    window.title("Game")
    calc_frame = ctk.CTkFrame(window, corner_radius=0)
    calc_frame.grid(column=0, row=0, sticky="nsew")
    chat_frame = ctk.CTkFrame(window, corner_radius=0)
    chat_frame.grid(column=1, row=0, sticky="nsew")
    window.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(chat_frame, text="Chat", font=("Consolas", 14), justify="left", anchor="w", height=40, width=100, text_color="#777").grid(row=0, column=0, pady=10, padx=10, sticky="w")
    NumberGuessing(
        calc_frame, chat_frame, window,
        ["+", "-", Calculator.mult, Calculator.div, "x^a", "Const", "(", ")", "ln", "sin", "tan", "cos", "|x|", ".", "%"]
    ).buildCalculator()

#More games coming soon...