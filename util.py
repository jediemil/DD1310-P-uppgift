import os
from dataclasses import dataclass


@dataclass
class Settings:
    grid_height: int
    grid_width: int
    torus: bool
    generations: int
    default_simulation_step: int


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_user_input_int_in_range(prompt, min_val, max_val, default=""):
    while True:
        answer = input(prompt) or default
        try:
            answer_int = int(answer)
            if min_val <= answer_int <= max_val:
                return answer_int
            else:
                clear_console()
                print(f"{answer_int} ligger inte mellan {min_val} och {max_val}")

        except ValueError:
            clear_console()
            print(f"\"{answer}\" är inte ett giltigt heltal")


def get_y_n_from_user(prompt, default=""):
    while True:
        answer = input(prompt).lower() or default
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Svaret måste vara y eller n")