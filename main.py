"""This is the main file.

Display a menu to call the function that resolve the questions.

Notes
-----
It was programmed in python 3.9.
Author: Jonathan Garcia.

To simplify the program, this was used modular programming, although
when modeling the tables with Peewee the 'POO' appears.

I used PEP 8 to the structure; but the characters' maximum per line it
was fixed in 120. The comments (and docstrings) lenght is 72.
Also, there are type hints in the functions (they are priorities) and
variables. Following the PEP 483, 484, 526...

The format of docstrings is NumPy/SciPy, following PEP 257.

The API used is 'PokeAPI' (https://pokeapi.co/). Just accept HTTP GET
requests and not need authentication.
"""
from typing import Dict

from api_functions import get_option_user
from auxiliar_functions import clear_screen

def menu() -> None:
    """Show a menu with the options to resolve each one of the questions:
    
    1. Number of pokemons with 'at' and double 'a' its name.
    2. How many pokemon species are able to procreate with Raichu?
    3. Maximum and minimum weight of first season fighting type pokemon
       (id: 1-151).
    """
    options: Dict[int, str] = {
        1: "Número de pokemons con 'at' y doble 'a' en su nombre.",
        2: 'La cantidad de especies de pokémon son capaces de procrear con Raichu.',
        3: 'Peso máximo y mínimo de los pokémon de tipo lucha de la primera temporada.',
        4: 'Salir.'
    }

    clear_screen()
    print('\t\t-Datos curiosos sobre los pokémon-')
    for number, option in options.items():
        print(f'{number}. {option}')
    option_selected: int = get_option_user()
    # print(option_selected)

if __name__ == '__main__':
    menu()
