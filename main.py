from dataclasses import dataclass
from math import inf
from Grid import Grid
from util import get_user_input_int_in_range, clear_console

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
        coords = set()
        file = open(filename, "r")
        for line in file.readlines():
            x, y = line.split(" ")
            coords.add((int(x), int(y)))
        file.close()
        return coords

    except FileNotFoundError:
        print("Inputfilen hittades inte. Har den blivit raderad? Avslutar programmet")
        exit()
    except ValueError:
        print(f"Felaktig indata i {filename} - skippar")
        return set()


def start_simulation(grid, settings):
    next_generation = 0
    for generation in range(settings.generations):
        if generation == next_generation:
            clear_console()
            print(grid)
            next_steps = get_user_input_int_in_range(
                f"Hur många steg vill du hoppa (default {settings.default_simulation_step})",
                1, inf, settings.default_simulation_step)
            next_generation = generation + next_steps

        grid.simulate_step(generation)


def main():
    clear_console()
    print("Välkommen till livet hos matematiska organismer")
    settings = get_user_settings()
    files = get_input_files()

    alive_cells_coords = set()
    for filename in files:
        input_coords = read_input_file(filename)
        if len(input_coords) != 0:
            alive_cells_coords = alive_cells_coords.union(input_coords)

    grid = Grid(settings.grid_width, settings.grid_height)
    grid.add_alive_cells(alive_cells_coords)

    start_simulation(grid, settings)


if __name__ == '__main__':
    main()
