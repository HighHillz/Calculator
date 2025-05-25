import customtkinter as ctk
import arithmatic
import games

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Home")
window.geometry("700x375")
window.resizable(0, 0)

ctk.CTkLabel(window, text="Calculator", font=("Consolas", 45, 'bold')).pack(pady=20)

arithmatic_btn = ctk.CTkButton(window, text="Arithmatic Calculator", width=200, height=40, font=('Consolas', 13), command=lambda: arithmatic.run(window)).pack(pady=5)

game_btn = ctk.CTkButton(window, text="Game", fg_color="green", hover_color="dark green", width=200, height=40, font=('Consolas', 13), command=lambda: games.run(window)).pack(pady=5)

window.mainloop()