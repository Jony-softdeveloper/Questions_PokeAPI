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
from pprint import pprint
from functions import menu, get_option_user
from pokemon import Pokemon
from request import PokeApi
def main() -> None:
    """Call menu and resolve the question."""
    menu()
    option_selected: int = get_option_user()
    print(option_selected)
    
    # review status_code
    # print(PokeApi(limit=1126).get_all_pokemon())
    
    # try:
    #     raichu: Pokemon = PokeApi().get_pokemon(id=26)
    # except AttributeError as atrribute_error:
    #     print(f'Lo sentimos ha ocurrido un error: {atrribute_error}')
    # else:
    #     egg_groups_species = PokeApi().get_egg_group_species(raichu)
    #     pprint(egg_groups_species)
    #     for value in egg_groups_species.values():
    #         print(len(value))
    # # validate thta egg_groups_species is not empty and eceptions JsonDecoder
    
    
if __name__ == '__main__':
    main()
