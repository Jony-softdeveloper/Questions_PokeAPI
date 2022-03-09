"""Auxiliar functions of the program."""
from os import system, name

def clear_screen() -> None:
    '''To clear screen terminal indepently of Operating system.

    Returns
    -------
    None
    '''
    system('cls' if name == 'nt' else 'clear')


def menu() -> int:
    """Show a menu with the options to resolve each one of the questions:
    
    1. Number of pokemons with 'at' and double 'a' its name.
    2. How many pokemon species are able to procreate with Raichu?
    3. Maximum and minimum weight of first season fighting type pokemon
       (id: 1-151).
    """
    options: dict[int, str] = {
        1: "Número de pokemons con 'at' y doble 'a' en su nombre.",
        2: 'La cantidad de especies de pokémon son capaces de procrear con Raichu.',
        3: 'Peso máximo y mínimo de los pokémon de tipo lucha de la primera temporada.',
        4: 'Salir.'
    }

    clear_screen()
    print('\t\t-Datos curiosos sobre los pokémon-')
    for number, option in options.items():
        print(f'{number}. {option}')

def get_option_user() -> int:
    """Get the option of the user.

    Returns
    -------
    option: int
        Number of option selected.
    """
    while True:
        try:
            option: int = int(input("\nElige un número de la inquietud que tengas de los 'Monstruos de bolsillo': "))
        except ValueError:
            print('Solo puedes ingresar números entre 1 y 4. Por favor reintentelo.')
            continue
        else:
            if option <= 0 or option > 4:
                print('Lo siento, está opción no existe. Por favor reintentelo.')
                continue
            break

    return option