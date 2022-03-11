"""This is the main file.

Display a menu to call the function that resolve the questions.

Notes
-----
It was programmed in python 3.10.2 (The last version).
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
from typing import NoReturn, Callable

from src.functions import (menu, get_option_user, print_option, notes, pokemon_match_patterns,
                        pokemon_egg_group_species, max_min_weigth_pokemon_by_type_generation, exit)

def main() -> None:
    """Call menu and resolve the question."""
    resolve: dict[int, Callable[[], int|list[float]|NoReturn]] = {
        1: pokemon_match_patterns,
        2: pokemon_egg_group_species,
        3: max_min_weigth_pokemon_by_type_generation,
        4: exit
    }

    while True:
        menu()
        result: int|list[float] = 0
        option_selected: int = get_option_user()
        if option_selected == 2:
            pokemon, result = resolve[option_selected]()  # type: ignore
            notes(option_selected, pokemon=pokemon)  # type: ignore
            print_option(option_selected, pokemon_name=pokemon.name) # type: ignore
        else:
            result = resolve[option_selected]()
            notes(option_selected)
            print_option(option_selected)
        print(result)
        
        to_continue: str = input(
            "\n¿Desea resolver alguna otra pokéduda? Sí (presione 's') o cualquier otra tecla para salir: "
            ).lower().strip()
        if to_continue == 's':
            continue
        else:
            exit()

if __name__ == '__main__':
    main()
