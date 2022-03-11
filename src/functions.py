"""Auxiliar functions of the program."""
from os import system, name
from typing import NoReturn, Any

from pandas import DataFrame
from requests.exceptions import JSONDecodeError # type: ignore

from pokemon import Pokemon
from request import PokeApi


def spanish_options(pokemon_name: str = 'raichu', type: str ='lucha', generation: int = 1) -> dict[int, str]:
    """Return a dict with the questions.

    The second option (key in dict) is a special case, because can
    receive the name of a pokemon.

    Parameters
    ----------
    pokemon_name: str, optional
        Name of pokemon to use in key 2.
    type: str, optional
        Type of pokemon to use in key 3.
    generation: int, optional
        Generation of pokemon to use in key 3.    
    Returns
    -------
    options: dict[int, str]
        The dictinary with the questions in spanis.h
    """
    options: dict[int, str] = {
        1: "El número de pokémons con 'at' y doble 'a' en su nombre.",
        2: f'La cantidad de especies de pokémons que son capaces de procrear con {pokemon_name.capitalize()}.',
        3: f'El peso máximo y mínimo de los pokémons de tipo {type} de la generación {generation}.',
        4: 'Salir.'
    }
    return options

def clear_screen() -> None:
    '''To clear screen terminal indepently of Operating system.

    Returns
    -------
    None
    '''
    system('cls' if name == 'nt' else 'clear')

def exit() -> NoReturn:
    """Finish the execution."""
    print("Ojalá hayas resuelto tus pokédudas. ¡Hasta pronto!")
    raise SystemExit  # Exactly the same to write system.exit

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

def list_pokemons_contain_pattern(pokemons: list[dict[str, str]], 
                                  pattern: str, is_regex: bool = False) -> DataFrame:
    """Return a dataframe of pokemons that match the pattern.

    Parameters
    ----------
    pokemons: list[dict[str, str]]
        List of dictionaries with pokemon data.
    pattern: str
        Pattern to find within names.
    is_regex: bool, optional
    Returns
    -------
    pokemons_with_pattern: DataFrame
        List of pokemons with the pattern.
    """
    df_pokemons = DataFrame(pokemons, columns=['name'], dtype=str)
    matching_pokemons = df_pokemons.loc[df_pokemons['name'].str.contains(pattern, regex=is_regex)]
    return matching_pokemons


def no_duplicates(pokemon_data_1: list[dict[str, Any]], pokemon_data_2: list[dict[str, Any]]|None = None,
                    type_join: str = 'outer') -> DataFrame:
    """Create from two list dictionaries data, usually with pokemon
    
    data, dataframes with the goal of merged and delete duplicate
    registers.

    Parameters
    ----------
    pokemon_data_1: list[dict[str, Any]]
        Dataframe 1 with the name of pokemons. 
    pokemon_data_2: list[dict[str, Any]]|None, optional
        Dataframe 2 with the name of pokemons.
    type_join: str
        The way pandas will perform the merge (join). 
        Te value by default is 'outer'.

    Returns
    -------
        The merge dataframe with no duplicates.
    """
    df_pokemon_1 : DataFrame = DataFrame(pokemon_data_1, columns=['name'], dtype=str)
    if pokemon_data_2 is None:
        return df_pokemon_1
    df_pokemon_2 : DataFrame = DataFrame(pokemon_data_2, columns=['name'], dtype=str)

    # Merge 'outer' on 'name' column avoid duplicates.
    df_merge: DataFrame = df_pokemon_1.merge(df_pokemon_2, on='name', how=type_join)
    # total_pokemons: int = df_merge['name'].count()
    # print(f'Total: {total_pokemons}')
    return df_merge

    
def pokemon_match_patterns(pattern_1: str = 'at', regex_1: str = '^(?:(?!a).)*a(?:(?!a).)*a(?:(?!a).)*$') -> int:
    """Resolve question 1 (read more in menu funtion).
    
    Parameters
    ----------
    pattern_1: str, optional
        Pattern to find within names. Default value is literal 'at'.
    regex_1: str, optional
        Regex to find within names of pokemons. 
        The default search for pokemon with double 'a'.

    Returns
    -------
    int 
        Number of pokemons that match with the patterns.
    
    Notes
    -----
    The names of pokemons takes account was the normal (towards id
    898), i.e. they weren't considered the  'mega' and 'vmax' ones;
    'alola' and 'galar' variations; etc.

    Also, the names are in its english version. So the final count
    could change according the language.
    """
    # '?:' in each group to indicate is non-capturing version of group
    # an thus avoid warning.
    try:
        all_pokemons: list[dict[str, str]]|None= PokeApi(limit=898).get_all_pokemon()
    except JSONDecodeError as jde:
        print(f'Ha surgido un error:\n{jde}')
    else:
        pokemons_at: DataFrame = list_pokemons_contain_pattern(all_pokemons, pattern_1)
        pokemons_double_a: DataFrame = list_pokemons_contain_pattern(all_pokemons, regex_1, is_regex=True)
        # print("'pokemons_at' + 'pokemons_double_a' =", end=' ')
        # print(pokemons_at['name'].count(), end=' + ')
        # print(pokemons_double_a['name'].count(), end=' = ')
        # print(pokemons_at['name'].count() + pokemons_double_a['name'].count())
        # duplicate: DataFrame = pokemons_at.merge(pokemons_double_a, on='name', how='inner')
        # number_duplicate = duplicate['name'].count()
        # print(f'Duplicados: {number_duplicate}')
        
        # Merge 'outer' on 'name' column avoid duplicates.
        df_merge: DataFrame = pokemons_at.merge(pokemons_double_a, on='name', how='outer')
        total_pokemons_patterns: int = df_merge['name'].count()
        # print(f'Total: {total_pokemons_patterns}')
        return total_pokemons_patterns

def pokemon_egg_group_species(id: int = 26) -> tuple[Pokemon, int]:
    """Resolve question 2 (read more in menu funtion).

    Say the number of species belonging to the egg groups of the
    pokemon id.

    Parameters
    ----------
    id: int, optional
        Id of the pokemon to check all the species belonging to its egg
        groups.
        Set in Raichu's Id by default.

    Returns
    -------
    tuple[Pokemon, int] 
        A tuple with the egg group(s)'s name(s) and the number of
        pokemons in both egg groups (witouth duplicates).
    """
    try:
        pokemon: Pokemon = PokeApi().get_pokemon(id)
    except AttributeError as atrribute_error:
        print(f'Ha surgido un error:\n{atrribute_error}')
    except JSONDecodeError as jde:
        print(f'Ha surgido un error:\n{jde}')
    else:
        egg_groups_species = PokeApi().get_egg_group_species(pokemon)
        # Pokemons with only one egg group.
        if len(egg_groups_species) == 1:  # type: ignore
            _ , egg_group_species = list(egg_groups_species.items())[0]  # type: ignore
            return pokemon, len(egg_group_species)
        # Pokemons with two egg groups
        egg_group_species_1, egg_group_species_2 = egg_groups_species.values()  # type: ignore
        total_species: DataFrame = no_duplicates(egg_group_species_1, egg_group_species_2)
        #print(total_species)
        number_total_species: int = total_species['name'].count()
        return pokemon, number_total_species

def max_min_weigth_pokemon_by_type_generation(type: str = 'fighting', generation: int = 1) -> list[float]:
    """Look for the highest and lowest weight within the pokémon
    
    according to a type of pokemon and a generation.

    Parameters
    ----------
    type: str, optional
        Type of pokemons of interest. Default value is 'fighting'.
    generation: int, optional
        The generation to cross with 'type' param. Default value is 1.

    Returns
    -------
    list[float]
        A list with the highest and lowest weight in the data get.
    
    Notes
    -----
    The position 0 is always the highest wight, whilst position 1,
    the lowest one.
    """
    list_pokemon_weight: list[float] = []
    try:
        pokemon_type: dict[str, list] = PokeApi().list_pokemon_by_type(type)
        pokemon_generacion: dict[str, list] = PokeApi().list_pokemon_generation(generation)
    except AttributeError as atrribute_error:
        print(f'Ha surgido un error:\n{atrribute_error}')
    except JSONDecodeError as jde:
        print(f'Ha surgido un error:\n{jde}')
    else:
        list_pokemon_type: list[dict[str, str]] = list(pokemon_type.values())[0]
        list_pokemon_generacion: list[dict[str, str]] = list(pokemon_generacion.values())[0]
        pokemon_type_generation: DataFrame = no_duplicates(
                                                list_pokemon_type, list_pokemon_generacion, type_join='inner')
        # Get the weight of each pokemon
        for pokemon_name in pokemon_type_generation['name']:
            pokemon: Pokemon = PokeApi().get_pokemon(pokemon_name)
            pokemon_weight: float = float(str(round(pokemon.weight, 2)))
            list_pokemon_weight.append(pokemon_weight)
        
        pokemon_type_generation['weight'] = list_pokemon_weight
        max_weight = pokemon_type_generation['weight'].max()
        min_weight = pokemon_type_generation['weight'].min()
        # print(pokemon_type_generation)
        return [max_weight, min_weight]
        
def print_option(option_selected: int, pokemon_name: str = 'raichu') -> None:
    """Shows the option selected by the user.

    Generally called along with your answer.

    Parameters
    ----------
    option_selected: int
        Number of option selected.
    pokemon_name: str, optional
        Name of pokemon to show in second question.
    """
    print(f'{option_selected}. {spanish_options(pokemon_name)[option_selected][:-1]} = ', end='')


def notes(number_question: int, **kwargs: int) -> None:
    """Display notes about the question selected by the user.

    Not all questions have notes.

    Parameters
    ----------
    number_question: int
        According the number of question, a specific note will be
        displayed.
    """
    print('Considere qué...')
    if number_question == 1:
        nota_1: str = (
            'El conteo de estos pokemon ser realizo con la versión en inglés de los nombres de los pokémons.')
        nota_2: str = (
            "Los pokémons tomados en cuenta son los que se listan normamelment. Es decir, que solo se considero\n"
            "\t  hasta el id 898, omitiendo completamente: los nombres 'mega' y 'vmax'; las variaciones de 'alola' y\n"
            "\t  'galar', etcétera.")
        print(f'\t• {nota_1}\n\t• {nota_2}\n')
    
    elif number_question == 2:
        if kwargs['pokemon'] is None:
            print(f"Una disculpa. Ha surgido un error debido a que no se encontró el parámetro 'nombres'.")
            return
        pokemon: Pokemon = kwargs['pokemon']  # type: ignore
        egg_groups: list[dict[str, str]] = pokemon.egg_groups
        print("Los pokémons pueden procrear siempre y cuando pertenezcan al mismo 'egg group'.")
        if len(egg_groups) == 1: # Pokemons with only one egg group
            egg_group_name = list(egg_groups[0].values())[0]
            print(f"{pokemon.name.capitalize()} pertenece a el grupo de huevo: '{egg_group_name}'.\n")
        else:
            egg_group_name_1: str = list(egg_groups[0].values())[0]
            egg_group_name_2: str = list(egg_groups[1].values())[0]
            print(
                f"{pokemon.name.capitalize()} pertenece a el grupo de huevos: '{egg_group_name_1}' y a "
                f"'{egg_group_name_2}.'\n")
    elif number_question == 3:
        print('Los pesos de los pokemón han sido convertidos a kilogramos.\n')

def menu() -> int:
    """Show a menu with the options to resolve each one of the questions:
    
    1. Number of pokemons with 'at' and double 'a' its name.
    2. How many pokemon species are able to procreate with Raichu?
    3. Maximum and minimum weight of first season fighting type pokemon
       (id: 1-151).
    """
    clear_screen()
    print('\t\t-Datos curiosos sobre los pokémon-')
    for number, option in spanish_options().items():
        print(f'{number}. {option}')