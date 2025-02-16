# Av Emil Reyier Hedin 2024-12-02. Senast ändrad 2025-02-16

from UserInterface import UserInterface


if __name__ == "__main__":
    # Startar programmet
    print("Startar programmet")
    ui = UserInterface()
    ui.start_game_loop()
    ui.start_ui()
    print("Programmet avslutat")
