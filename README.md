# Version 2 - Game Suite

An interactive, sleek, GUI-based suite built with CustomTkinter in Python. The application features a scientific/arithmetic calculator with interactive history tracking and an integrated number-guessing game played against a bot.

![Latest Version](https://img.shields.io/badge/Latest%20Version-2.0.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Inactive-yellow.svg)

## 🌟 Features

### 1. Scientific & Arithmetic Calculator (`calculator.py`)
* **Standard & Scientific Operations**: Supports standard arithmetic operations alongside functions like exponents ($x^a$), natural log ($ln$), absolute values ($|x|$), percentages (%), and trigonometry (sin, cos, tan).
* **Mathematical Constants**: Supports quick insertions of mathematical constants like $e$ and $\pi$ via a separate overlay window.
* **Custom Layout System**: Built on a modular grid component framework utilizing CustomTkinter's modern dark theme widgets.

### 2. Live Calculation History (`arithmetic.py`)
* **Interactive History Sidebar**: Keeps a running log of all evaluated equations and results in a scrollable frame.
* **Calculation Restoration**: Clicking on any historical calculation card automatically loads that equation and its result back into the calculator interface.

### 3. Integrated Guess the Number Game (`games.py`)
* **Calculator input as game controller**: Uses the calculator's numeric keypad for inputting guesses.
* **SigmaBot Opponent**: Play against a bot called "SigmaBot". You have 7 chances to guess a random number between 1 and 100.
* **Score Tracker**: Displays real-time game scores tracking your wins versus SigmaBot's wins.

## 🚀 Setup & Installation

### Prerequisites
Make sure you have **Python 3.12+** and the Python Tkinter system library installed.
* On Debian/Ubuntu:
  ```bash
  sudo apt-get install python3-tk
  ```

### Installation
1. Clone this repository (or navigate to its directory).
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   ```
3. Install the dependencies:
   ```bash
   pip install customtkinter
   ```

## 🎮 How to Run

Run the launcher application from your terminal:
```bash
python3 home.py
```
*(Or `./venv/bin/python3 home.py` if running directly using the virtual environment's path).*
