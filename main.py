# Av Emil Reyier Hedin 2024-11-21. Senast ändrad 2025-02-20

from math import inf
from Grid import Grid
from util import get_user_input_int_in_range, clear_console, get_j_n_from_user, Settings


# Konstanter
MIN_HEIGHT = 5
MAX_HEIGHT = 200
MIN_WIDTH = 5
MAX_WIDTH = 200


def get_user_settings():
    """Funktionen frågar användaren efter varje tillgänglig inställning och returnerar en ny Settings dataklass
    som innehåller användarens svar.
    :return: Settings() -> Innehåller användarens svar.
    :rtype: Settings"""

    print("Nu behövs några inställningar för att kunna köra programmet korrekt")
    height = get_user_input_int_in_range("Hur högt vill du ha spelbrädet? \n", MIN_HEIGHT, MAX_HEIGHT)
    clear_console()
    width = get_user_input_int_in_range("Hur brett vill du ha spelbrädet? \n", MIN_WIDTH, MAX_WIDTH)
    clear_console()
    torus = get_j_n_from_user("Vill du att spelbrädet ska bete sig som en torus, alltså att höger kant är"
                              " granne med vänster kant, och övre kanten är granne med undre kanten (j/n)\n")
    clear_console()
    num_generations = get_user_input_int_in_range("Hur många generationer vill du simulera? \n", 1, inf)
    clear_console()
    generation_step = get_user_input_int_in_range("Hur många generationer vill du stega? (1 default)\n"
                                                  "Tryck på enter för att välja default.\n", 1, inf, "1")
    clear_console()
    # Skapar en settings dataklass och returnerar den på samma rad
    return Settings(height, width, torus, num_generations, generation_step)


def get_input_files():
    """Funktionen frågar användaren efter filer som innehåller datan för var celler ska placeras.
    Användaren får skriva in hur många filer som helst, men minst en fil. Om användaren skriver in en
    fil som inte existerar frågas användaren på nytt efter filer. Funktionen returnerar en lista med namnet
    på alla giltiga filer.
    :return: set[str] -> En lista med filnamn
    :rtype: set[str]"""

    files = set()
    print("Vänligen skriv in namnet på den fil som innehåller koordinaterna till de levande cellerna")
    while True:
        filename = input()

        if filename == "":  # Om användaren bara trycker på enter utan att skriva något
            if len(files) == 0:
                # Om användaren inte har gett en fil så frågas den igen.
                print("Du måste ange minst 1 fil")
                continue
            # Om användaren redan har angett minst en fil avslutas loopen.
            break

        try:  # Kolla att filen finns innan den läggs till i mängden av filer.
            file = open(filename, "r")
            file.close()
            files.add(filename)
            print("Ange nästa fil, lämna tomt för att avsluta")
        except FileNotFoundError:
            print("Kunde inte hitta filen")

    return files


def read_input_file(filename, settings):
    """Funktionen tar in ett filnamn och läser celldatan i filen. Koordinaterna i filen
    valideras och funktionen returnerar ett set med alla koordinater som ska innehålla levande
    celler.
    :param filename: Namn på filen som innehåller koordinaterna
    :type filename: str
    :param settings: Settings dataklass med användarens inställningar
    :type settings: Settings
    :return: set[tuple[int, int]] -> Ett set med koordinaterna till de levande cellerna i formen av tuples
    :rtype: set[tuple[int, int]]"""

    try:  # En try-except här för att skydda mot formatfel i filerna
        coords = set()
        file = open(filename, "r")
        for line in file.readlines():
            # Varje rad ska ha två tal separerade med blanksteg, det motsvarar x, och y koordinaterna.
            x_str, y_str = line.split(" ")
            x, y = int(x_str), int(y_str)

            # Validera att koordinaterna ligger inom brädet.
            if 0 <= x < settings.grid_width and 0 <= y < settings.grid_height:
                coords.add((x, y))
            else:
                print(f"Koordinaterna {x}, {y} i {filename} ligger inte innanför spelbrädet - skippar filen")
                file.close()
                # Om det blir fel kan ett tomt set returneras, så skadas inte resten av programmet.
                return set()

        file.close()
        return coords

    except ValueError:
        print(f"Felaktig indata i {filename} - skippar")
        return set()


def start_simulation(grid, settings):
    """Funktionen startar simulationen och kör den i så många generationer som användaren specificerat.
    Mellan varje generation frågas användaren hur många generationer som ska simuleras innan nästa utskrift.
    :param grid: Grid objekt som simulationen sker på
    :type grid: Grid
    :param settings: Användarens inställningar
    :type settings: Settings"""

    next_generation = 0  # next_generation motsvarar nästa generation som ska få en full utskrift
    input("Klicka på enter för att starta...")  # Väntar på användaren.
    for generation in range(settings.generations):
        if generation == next_generation:
            # Skriver ut griden om nuvarande generation är den som ska printas.
            clear_console()
            print(grid)

            # Frågar användaren hur många generationer som ska simuleras innan nästa utskrift.
            next_steps = get_user_input_int_in_range(
                f"Hur många steg vill du hoppa (default {settings.default_simulation_step})",
                1, inf, settings.default_simulation_step)
            next_generation = generation + next_steps

        grid.simulate_step(generation)  # Simulerar en generation

    clear_console()
    print(grid)
    input("Detta var den sista generationen, klicka på enter för att avsluta...")


def main():
    """Funktionen välkomnar användaren, frågar om inställningar och filer,
    skapar ett grid, lägger in cellerna i griden, och startar sedan simulationen. När
    simulationen är klar avslutas programmet."""

    clear_console()
    print("Välkommen till livet hos matematiska organismer")
    settings = get_user_settings()  # Hämtar inställningar
    files = get_input_files()  # Hämtar filer

    alive_cells_coords = set()  # En mängd av alla koordinater som ska innehålla levande celler
    # Loopar genom alla filer som användaren angett och lägger till koordinaterna till alive_cells_coords
    for filename in files:
        input_coords = read_input_file(filename, settings)
        if len(input_coords) != 0:
            alive_cells_coords = alive_cells_coords.union(input_coords)

    if len(alive_cells_coords) == 0:
        # Här kan programmet hamna ifall det var fel i filerna som användaren angav.
        print("Inga levande celler lades till, avslutar programmet")
        exit()

    grid = Grid(settings.grid_width, settings.grid_height, settings.torus)  # Skapar ett grid
    grid.add_alive_cells(alive_cells_coords)  # Lägger in de levande cellerna i griden

    start_simulation(grid, settings)

    print("Tack för att du använde programmet")


if __name__ == '__main__':  # Startar programmet ifall denna fil körs med python.
    main()
