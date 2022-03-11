"""Classes which permit make the request to Pokemon API enpoints."""
from typing import Any
import requests
from requests.exceptions import JSONDecodeError

from pokemon import Pokemon

class RequestApi():
    """Model the general data and functionality to make a request.
    
    Attributes
    ----------
    base_url: str
        The base URL of the API.
    
    Notes
    -----
    At the moment is just defined the GET methos, but is possible
    define any other.
    """

    def __init__(self, base_url: str) -> None:
        """Initialize the attributes.
        
        Parameters
        ----------
        base_url: str
            The base URL of the API. 

        Notes
        -----
        The base_url must to be finished in '/'.
        """
        self.base_url: str = base_url

    def get(self, endpoint_url: str, **kwargs: int) -> requests.Response:
        """Get data from and specific endpoint."""
        return requests.get(f'{self.base_url}{endpoint_url}', **kwargs)


class PokeApi(RequestApi):
    """Request to the PokeApi and process the data.

    Attributes
    ----------
    base_url: str
        The base URL of the API. In this case by default is the PokeAPI
        url. 
    limit: int
        Indicate the number of resources to get by page. It is a query
        parameter.

    Notes
    ----- 
    The PokeAPI only accept GET request, so it isn' necessary write
    any other. Besides is a public API, so doesn't need authentication.
    """

    def __init__(self, base_url: str= 'https://pokeapi.co/api/v2/', **kwargs: int) -> None:
        """Initialize the attributes.
        
        Parameters
        ----------
        base_url: str, optional
            The base URL of the PokeAPI.
        kwargs: dict
            Other parameters to create a request.

        Notes
        -----
        The base_url must to be finished in '/'.
        """
        super().__init__(base_url)
        self.limit: int = kwargs.get('limit', 10)  # By default is 10
        
    def get_all_pokemon(self) -> list[dict[str, str]]|None:
        """Obtain -in only one request- the 'list' of all pokemon.

        Returns
        -------
        list[dict[str, str]]
            Contain the name of every pokemon registered.
        """
        endpoint_url: str = 'pokemon/'
        params: dict[str, int] = {'limit': self.limit}

        response = self.get(endpoint_url, params=params)  # type: ignore
        if response.status_code == 200:
            json_response: dict[str, Any] = self.json_response(response, 'get_all_pokemon')
            return json_response['results']

        print(f"Una disculpa. Ha ocurrido un error al intentar obtener la lista de todos los pokémons.")

    def json_response(self, response: requests.Response, method_name: str) -> dict[str, Any]:
        """Try to convert the response to a JSON. In case it wasn't
        
        possible, set a message to re-raise the exception
        JSONDecodeError according the method where it is called.
        
        Paramaters
        ----------
        response: requests.Response
            Request response to PokeAPI. Object that can raise
            JSONDecodeError when is trying to deserialize it.
        method_name: str
            Name of method where the exception is raised.

        Returns
        -------
        dict[str, Any]
            The content of the response transformed in a JSON.

        Raises
        ------
        JSONDecodeError
            If the response contains invalid JSON.
        """
        try:
            return response.json()
        except JSONDecodeError: 
            raise JSONDecodeError(f"There was a problem deserializing the request response in '{method_name}'.")
            

    def get_pokemon(self, id: int = 0, name: str = '') -> Pokemon|None:
        """Get the data of a pokemon data according its either id
        
        or name.
        
        Parameters
        ----------
        id: int, optional
            Pokemon's ID which is looking for.
        name: str, optional
            Pokemon's name which is looking for.

        Returns
        -------
        pokemon: Pokemon
            The instance of a pokemon with id, name, weight, height and
            egg_groups.
        """
        endpoint_url: str ='pokemon-species/'
        weight: float = 0
        height: float = 0

        if not id and not name:
            raise AttributeError(f"A parameter 'id' or 'name' is required.")
        elif id and name:
            raise AttributeError(f"It was provided both parameters 'id' and a 'name'. Please just input one of them.")
        
        response: requests.Response = self.get(f'{endpoint_url}{id}/') if id else self.get(f'{endpoint_url}{name}/')
        if response.status_code == 200:
            json_response: dict[str, Any] = self.json_response(response, 'get_pokemon')
            egg_groups: list[dict[str,str]] = json_response['egg_groups']
            weight, height = self.get_weight_height_pokemon(id=id) if id else self.get_weight_height_pokemon(name=name)

            return Pokemon(
                id=json_response['id'],
                name=json_response['name'],
                weight=weight,
                height=height,
                egg_groups=egg_groups)
        
        elif id:
            print(f"Una disculpa. Ha ocurrido un error al intentar obtener el pokémon con id: {id}.")
        else:
            print(f"Una disculpa. Ha ocurrido un error al intentar obtener el pokémon con el nombre: {name}.")


    def get_weight_height_pokemon(self, id: int = 0, name: str = '') -> tuple[float, float]:
        """Get the wight and height of the pokemon through its id

        or name.
        
        Parameters
        ----------
        id: int, optional
            Pokemon's ID which is looking for.
        name: str, optional
            Pokemon's name which is looking for.

        Returns
        -------
        tuple[float, float]
            A tuple with both values: (weight, height) 

        Notes
        -----
        The values return are converted from hectograms to kilograms
        (weight) and from hectimeters to meters (height).
        """
        endpoint_url: str = 'pokemon/'
        if not id and not name:
            raise AttributeError(f"A parameter 'id' or 'name' is required.")
        elif id and name:
            raise AttributeError(f"It was provided both parameters 'id' and a 'name'. Please just input one of them.")

        response: requests.Response = self.get(f'{endpoint_url}{id}/') if id else self.get(f'{endpoint_url}{name}/')
        if response.status_code == 200:
            json_response: dict[str, Any] = self.json_response(response, 'get_weight_height_pokemon')
            weight: float = json_response['weight'] * 0.1   # type: ignore
            height: float = json_response['height'] * 0.1   # type: ignore
            return weight, height


    def get_spanish_name(self, list_languages_names: list[dict[str, Any]]) -> str|None:
        """Search within a list of dicts for that dict which refers to
        
        spanish language and get the interest data.

        Parameters
        ----------
        list_languages_names: list[dict[str, Any]]
            List of dicts that contains the data in distinct languages.

        Returns
        -------
        str
            The name in spanish, in case exists.
        """
        for group_name in list_languages_names:
            if group_name['language']['name'] == 'es':
                return group_name['name']

    def set_values_dict(self, json_response: dict[str, Any],
                        concept_value: str|int, key_word: str) -> tuple[str|int, list[dict[str, Any]]]:
        """Set name of of the concept being treated and a list of 
        
        dictionaries with the values of interest (key). Both values
        are returned.

        Parameters
        ----------
        json_response: dict[str, Any]
            The content of a response transformed to JSON.
        concept_value: str|int
            In case it won't be possible get the name in spanish, the
            concept value will work as name.
        key_word: str
            Indicate the key to search inside the json response.

        Responses
        ---------
        tuple[str|int, list[dict[str, Any]]]
            Name of the concept and the list of dictionaries with
            the values searched.

        Notes
        -----
        The most of the time the 'key' is about pokemon, that's the
        reason the variable named as 'pokemon_something'.
        """
        concept_languages_names: list[dict[str, Any]] = json_response['names']
        concept_name: str|int = self.get_spanish_name(concept_languages_names) or concept_value
        return (concept_name, json_response[key_word])

    def get_egg_group_species(self, pokemon: Pokemon)-> dict[str, list]|None:
        """Get the species that belongs to the same egg group.
        
        The species in the group are able to group with the pokemon.

        Parameters
        -----------
        pokemon: Pokemon
            The instance of a pokemon with id, name and egg_groups.

        Returns
        -------
        egg_group_species: dict[str, list]
            A dictionary where the keys are the egg groups' names and
            the values are lists which contain the species belonging to
            the egg group.
        """
        endpoint_url: str = 'egg-group/'
        egg_group_species: dict[str, list] = {}
        egg_groups: list[dict[str, str]] = pokemon.egg_groups

        for egg_group in egg_groups:
            name = egg_group['name']
            response: requests.Response = self.get(f'{endpoint_url}{name}/')
            if response.status_code == 200:
                json_response: dict[str, Any] = self.json_response(response, 'get_egg_group_species')
                egg_group_name, species_list = self.set_values_dict(json_response, name, 'pokemon_species')    
                # Add data to egg_group_species
                egg_group_species.setdefault(str(egg_group_name), species_list)
            else:
                print(f"Una disculpa. Ha ocurrido un error al intentar obtener el grupo de huevo '{name}'.")
                return None

        return egg_group_species

    def list_pokemon_by_type(self, type: str = '') -> dict[str, list]|None:
        """Retrieve in a list the name of all pokemons belonging to
        
        the type.

        Parameters
        ----------
        type: str, optional
            Name of type to search its pokemons.

        Returns
        --------
        pokemons_of_type: dict[str, list]
            The key is the name of type -whether possible in spanish-
            and the value is a list with the name of all pokemons of
            the type.
        """
        endpoint_url: str = 'type/'
        pokemons_of_type: dict[str, list] = {}
        if not type:
            raise AttributeError(f"The 'type' parameter is required.")
        
        response = self.get(f'{endpoint_url}{type}/')
        if response.status_code == 200:
            json_response: dict[str, Any] = self.json_response(response, 'list_pokemon_by_type')
            type_name, pokemon_dd_list = self.set_values_dict(json_response, type, 'pokemon')  # dd is refers to dict_dict 
            pokemon_dict_list: list[dict[str, str]] = [pokemon['pokemon'] for pokemon in pokemon_dd_list]
                
            # Add the data to the dict
            pokemons_of_type.setdefault(str(type_name), pokemon_dict_list)
            return pokemons_of_type

        print(f"Una disculpa. Ha ocurrido un error al generar la lista de los pokémons de tipo '{type}'.")

    def list_pokemon_generation(self, generation_number: int = 1) -> dict[str, list]|None:
        """Generate a list with the names of each pokemon of that
        
        specific generation.

        Parameters
        ----------
        generation_number: int, optional
            Number generation. It can be greater than 8.

        Returns
        --------
        pokemons_of_generation: dict[str, list]
            The key is the name of generation, in spanish if possible,
            and the value is the list with the names.
        """
        endpoint_url: str = 'generation/'
        pokemons_of_generation: dict[str, list] = {}

        if generation_number < 1 and generation_number > 8:
            print(f"El número de la generación solo puede estar entre 1 y 8. El '{generation_number}' no es valido.")
            return None
        response = self.get(f'{endpoint_url}{generation_number}/')
        
        if response.status_code == 200:
            json_response: dict[str, Any] = self.json_response(response, 'list_pokemon_generation')
            generation_name, pokemon_list = self.set_values_dict(json_response, generation_number, 'pokemon_species')
            pokemons_of_generation.setdefault(str(generation_name), pokemon_list)
            return pokemons_of_generation
        
        print(
            f"Una disculpa. Ha ocurrido un error al generar la lista de los pokémons de la "
            "generación '{generation_number}'.")

