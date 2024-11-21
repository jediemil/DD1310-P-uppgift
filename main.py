import os
from dataclasses import dataclass
from math import inf

MIN_HEIGHT = 5
MAX_HEIGHT = 10000
MIN_WIDTH = 5
MAX_WIDTH = 10000

@dataclass
class Settings:
    grid_height: int
    grid_width: int
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


def get_user_settings():
    print("Nu behövs några inställningar för att kunna köra programmet korrekt")
    height = get_user_input_int_in_range("Hur högt vill du ha spelbrädet? \n", MIN_HEIGHT, MAX_HEIGHT)
    clear_console()
    width = get_user_input_int_in_range("Hur brett vill du ha spelbrädet? \n", MIN_WIDTH, MAX_WIDTH)
    clear_console()
    num_generations = get_user_input_int_in_range("Hur många generationer vill du simulera? \n", 1, inf)
    clear_console()
    generation_step = get_user_input_int_in_range("Hur många generationer vill du stega? (1 default)\n"
                                                  "Tryck på enter för att välja default.\n", 1, inf, "1")
    clear_console()
    return Settings(height, width, num_generations, generation_step)


def get_input_files():
    files = set()
    print("Vänligen skriv in namnet på den fil som innehåller koordinaterna till de levande cellerna")
    while True:
        filename = input()

        if filename == "":
            if len(files) == 0:
                print("Du måste ange minst 1 fil")
                continue
            break

        try:
            file = open(filename, "r")
            file.close()
            files.add(filename)
            print("Ange nästa fil, lämna tomt för att avsluta")
        except FileNotFoundError:
            print("Kunde inte hitta filen")

    return files


def read_input_file(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("Inputfilen hittades inte. Har den blivit raderad? Avslutar programmet")
        exit()


def main():
    clear_console()
    print("Välkommen till livet hos matematiska organismer")
    settings = get_user_settings()
    files = get_input_files()
    print(files)



if __name__ == '__main__':
    main()