# Av Emil Reyier Hedin 2024-11-26. Senast ändrad 2025-02-16

import os
from dataclasses import dataclass


# En dataklass är som en lättare klass som är bra för att skicka data strukturerat. Kan jämföras med struct från C
@dataclass
class Settings:
    grid_height: int
    grid_width: int
    torus: bool
    generations: int
    default_simulation_step: int


def clear_console():
    """Funktionen ropar på operativsystemets inbyggda funktion för att tömma konsolen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_user_input_int_in_range(prompt, min_val, max_val, default=""):
    """Frågar användaren efter ett heltal inom ett intervall. Om användaren matar in
    ett ogiltigt tal eller ett tal utanför intervallet frågas användaren efter en ny input.
    Det går att sätta default, vilket är värdet som kommer att antas om användaren bara
    klickar på enter.
    :param prompt: Frågan som användaren ska få.
    :type prompt: str
    :param min_val: Det minsta värdet som användaren får mata in
    :type min_val: int
    :param max_val: Det största värdet som användaren får mata in
    :type max_val: int
    :param default: En sträng med det värdet som ska antas om användaren inte skrivet något
    :type default: str
    :returns: Ett heltal inom det accepterade intervallet.
    :rtype: int"""

    while True:
        answer = input(prompt) or default  # Om användaren svarar med en tom sträng väljs default istället
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
    """Funktionen frågar användaren om ett ja eller nej (y/n) och frågar igen tills
    en giltig inmatning uppnåts. Funktionen returnerar True om användaren skarade ja och False om användaren svarade nej.
    :param prompt: Frågan som ska ställas till användaren.
    :type prompt: str
    :param default: Kan sättas till 'y'/'n' för att välja det som default om användaren trycker på enter.
    :type default: str
    :returns: True om ja, False om nej
    :rtype: bool"""
    while True:
        answer = input(prompt).lower() or default
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Svaret måste vara y eller n")
