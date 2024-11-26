from dataclasses import dataclass
from math import inf
from Grid import Grid
from util import get_user_input_int_in_range, clear_console, get_y_n_from_user

MIN_HEIGHT = 5
MAX_HEIGHT = 10000
MIN_WIDTH = 5
MAX_WIDTH = 10000


@dataclass
class Settings:
    grid_height: int
    grid_width: int
    torus: bool
    generations: int
    default_simulation_step: int


def get_user_settings():
    print("Nu behövs några inställningar för att kunna köra programmet korrekt")
    height = get_user_input_int_in_range("Hur högt vill du ha spelbrädet? \n", MIN_HEIGHT, MAX_HEIGHT)
    clear_console()
    width = get_user_input_int_in_range("Hur brett vill du ha spelbrädet? \n", MIN_WIDTH, MAX_WIDTH)
    clear_console()
    torus = get_y_n_from_user("Vill du att spelbrädet ska bete sig som en torus, alltså att höger kant är"
                              "granne med vänster kant, och övre kanten är granne med undre kanten (y/n)\n")
    clear_console()
    num_generations = get_user_input_int_in_range("Hur många generationer vill du simulera? \n", 1, inf)
    clear_console()
    generation_step = get_user_input_int_in_range("Hur många generationer vill du stega? (1 default)\n"
                                                  "Tryck på enter för att välja default.\n", 1, inf, "1")
    clear_console()
    return Settings(height, width, torus, num_generations, generation_step)


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


def read_input_file(filename, settings):
    try:
        coords = set()
        file = open(filename, "r")
        for line in file.readlines():
            x_str, y_str = line.split(" ")
            x, y = int(x_str), int(y_str)
            if 0 <= x < settings.grid_width and 0 <= y < settings.grid_height:
                coords.add((x, y))
            else:
                print(f"Koordinaterna {x}, {y} i {filename} ligger inte innanför spelbrädet - skippar filen")
                file.close()
                return set()

        file.close()
        return coords

    except ValueError:
        print(f"Felaktig indata i {filename} - skippar")
        return set()


def start_simulation(grid, settings):
    next_generation = 0
    input("Klicka på enter för att starta...")
    for generation in range(settings.generations):
        if generation == next_generation:
            clear_console()
            print(grid)
            next_steps = get_user_input_int_in_range(
                f"Hur många steg vill du hoppa (default {settings.default_simulation_step})",
                1, inf, settings.default_simulation_step)
            next_generation = generation + next_steps

        grid.simulate_step(generation)

    clear_console()
    print(grid)
    input("Detta var den sista generationen, klicka på enter för att avsluta...")


def main():
    clear_console()
    print("Välkommen till livet hos matematiska organismer")
    settings = get_user_settings()
    files = get_input_files()

    alive_cells_coords = set()
    for filename in files:
        input_coords = read_input_file(filename, settings)
        if len(input_coords) != 0:
            alive_cells_coords = alive_cells_coords.union(input_coords)

    if len(alive_cells_coords) == 0:
        print("Inga levande celler lades till, avslutar programmet")
        exit()

    grid = Grid(settings.grid_width, settings.grid_height, settings.torus)
    grid.add_alive_cells(alive_cells_coords)

    start_simulation(grid, settings)

    print("Tack för att du använde programmet")


if __name__ == '__main__':
    main()
