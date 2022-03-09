"""Classes which permit make the request to Pokemon API enpoints."""
from typing import Optional
from abc import ABC, abstractmethod 

import requests
from requests.exceptions import JSONDecodeError
from pokemon import Pokemon

class RequestApi(ABC):
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

    def get(self, endpoint_url: str, **kwargs: dict[any, any]) -> requests.Response:
        """Get data from and specific endpoint."""
        return requests.get(f'{self.base_url}{endpoint_url}', **kwargs)

    # @abstractmethod
    # def process() -> None:
    #     """Define in a subclass.
        
    #     Process data received from the endpoints.
    #     """
    #     pass


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

    def __init__(self, base_url: str= 'https://pokeapi.co/api/v2/', **kwargs: dict[any, any]) -> None:
        """Initialize the attributes.
        
        Parameters
        ----------
        base_url: str
            The base URL of the PokeAPI.
        kwargs: dict
            Other parameters to create a request.

        Notes
        -----
        The base_url must to be finished in '/'.
        """
        super().__init__(base_url)
        self.limit: int = kwargs.get('limit', 10)  # By default is 10
        
    def get_all_pokemon(self) -> requests.Response:
        """Obtain -in only one request- the 'list' of all pokemon.

        Returns
        -------
        requests.Response
            The request response.
        """
        endpoint_url: str ='pokemon/'
        params: dict[str, int] = {'limit': self.limit}
        return self.get(endpoint_url, params=params)

    def get_pokemon(self, id: int = 0, name: str = '') -> Pokemon:
        """Get the data of a pokemon species according its either id
        
        or name.
        
        Parameters
        ----------
        id: int
            Pokemon's ID which is looking for.
        name: str
            Pokemon's name which is looking for.

        Returns
        -------
        pokemon: Pokemon
            The instance of a pokemon with id, name and egg_groups.
        """
        endpoint_url: str ='pokemon-species/'
        if not id and not name:
            raise AttributeError(f"A parameter 'id' or 'name' is required.")
        elif id and name:
            raise AttributeError(f"It was provided both parameters 'id' and a 'name'. Please just input one of them.")
        
        response: requests.Response = self.get(f'{endpoint_url}{id}/') if id else self.get(f'{endpoint_url}{name}/')
        if response.status_code == 200:
            try:
                json_response: dict[any, any] = response.json()
            except JSONDecodeError: 
                raise JSONDecodeError("There was a problem deserializing the request response in 'get_pokemon'.")
            egg_groups: dict[str, str] = json_response['egg_groups']
            return Pokemon(id=json_response['id'], name=json_response['name'], egg_groups=egg_groups)
        else:
            if id:
                print(f"Ha ocurrido un error al intentar obtener el pokemon con id: {id}. Lo lamentamos.")
            else:
                print(f"Ha ocurrido un error al intentar obtener el pokemon con el nombre: {name}. Lo lamentamos.")
            return None

    def get_spanish_name(self, list_languages_names: list[dict[str, any]]) -> Optional[str]:
        """Search within a list of dicts for that dict which refers to
        
        spanish language and get the interest data.

        Parameters
        ----------
        list_languages_names: list[dict[str, any]]
            List of dicts that contains the data in distinct languages.

        Returns
        -------
        Optional[str]
            The name in spanish, in case exists.
        """
        for group_name in list_languages_names:
            if group_name['language']['name'] == 'es':
                return group_name['name']
        return None

    def set_values_dict(self, json_response: dict[str, any],
                        concept_value: any, key_word: str) -> tuple[str, list[str]]:
        """Set name of of the concept being treated and a list with
        
        the values of interest (key). Both values are returned.

        Parameters
        ----------
        json_response: dict[str, any]
            It is the result of a request to the PokeApi tranformed to
            JSON.
        concep_value: any
            In case it won't be possible get the name in spanish, the
            concept value will work as name.
        key_word: str
            Indicate the key to search inside the response.

        Notes
        -----
        The most of the time the 'key' is about pokemon, that's the
        reason the variable named as 'pokemon_something'.
        """
        # Set concept name
        concept_languages_names: list[dict[str, any]] = json_response['names']
        concept_name = self.get_spanish_name(concept_languages_names) or concept_value
        # Set the list of pokemons
        pokemon_dict_list: list[dict[str,str]] = json_response[key_word]
        pokemon_list: list[str] = [pokemon['name'] for pokemon in pokemon_dict_list]

        return (concept_name, pokemon_list)

    def get_egg_group_species(self, pokemon: Pokemon)-> dict[Optional[str], Optional[list]]:
        """Get the species that belongs to the same egg group.
        
        The species in the group are able to group with the pokemon.

        Parameters
        -----------
        pokemon: Pokemon
            The instance of a pokemon with id, name and egg_groups.

        Returns
        -------
        egg_group_species: dict[Optional[str], Optional[list]]
            A dictionary where the keys are the egg groups' names and
            the values are lists which contain the species belonging to
            the egg group.
        """
        endpoint_url: str = 'egg-group/'
        egg_group_species: dict[Optional[str], Optional[list]] = {}
        
        for egg_group in pokemon.egg_groups:
            name = egg_group['name']
            response: requests.Response = self.get(f'{endpoint_url}{name}/')
            if response.status_code == 200:
                try:
                    json_response: dict[any, any] = response.json()
                except JSONDecodeError:
                    raise JSONDecodeError(
                        "There was a problem deserializing the request response in 'get_egg_group_species'.")
                
                # # Set group name
                # egg_group_languages_names: list[dict[str, str]] = json_response['names']
                # egg_group_name: str = self.get_spanish_name(egg_group_languages_names) or name
                # # Set species of egg group
                # species_dict_list: list[dict[str, str]] = json_response['pokemon_species']
                # species_list : list[str] = [group['name'] for group in species_dict_list]

                egg_group_name, species_list = self.set_values_dict(json_response, name, 'pokemon_species')
                # Add data to egg_group_species
                egg_group_species.setdefault(egg_group_name, species_list)
            
            else:
                print(f"Ha ocurrido un error al intentar obtener el grupo de huvo '{name}'. Lo lamentamos.")
                return None

        return egg_group_species

    def list_pokemon_by_type(self, type: str = '') -> dict[Optional[str], Optional[list]]:
        """Retrieve in a list the name of all pokemons belonging to
        
        the type.

        Parameters
        ----------
        type: str
            Name of type to search its pokemons.

        Returns
        --------
        pokemons_of_type: dict[Optional[str], Optional[list]]
            The key is the name of type -whether possible in spanish-
            and the value is a list with the name of all pokemons of
            the type.
        """
        endpoint_url: str = 'type/'
        pokemons_of_type: dict[Optional[str], Optional[list]] = {}

        if not type:
            raise AttributeError(f"The 'type' parameter is required.")
        
        response = self.get(f'{endpoint_url}{type}/')
        if response.status_code == 200:
            try:
                json_response: dict[any, any] = response.json()
            except JSONDecodeError:
                raise JSONDecodeError(
                    "There was a problem deserializing the request response in 'list_pokemon_by_type'.")
            # Set type name
            type_languages_names: list[dict[str, any]] = json_response['names']
            type_name = self.get_spanish_name(type_languages_names) or type
            # Set the list of pokemons
            pokemon_dict_list: list[dict[str,str]] = json_response['pokemon']
            pokemon_list: list[str] = [pokemon['pokemon']['name'] for pokemon in pokemon_dict_list]
            
            # Add the data to the dict
            pokemons_of_type.setdefault(type_name, pokemon_list)
        
        return pokemons_of_type

    def list_pokemon_generation(self, generation_number: int = 1) -> Optional[dict[Optional[str], Optional[list]]]:
        """Generate a list with the names of each pokemon of that
        
        specific generation.

        Parameters
        ----------
        generation_number: int
            Number generation. It can be greater than 8.

        Returns
        --------
        pokemons_of_generation: dict[Optional[str], Optional[list]]
            The key is the name of generation, in spanish if possible,
            and the value is the list with the names.
        """
        endpoint_url: str = 'generation/'
        pokemons_of_generation: dict[Optional[str], Optional[list]] = {}

        if generation_number < 1 and generation_number > 8:
            print(f"El número de la generación solo puede estar entre 1 y 8. El '{generation_number}' no es valido.")
            return None
        response = self.get(f'{endpoint_url}{generation_number}/')
        
        if response.status_code == 200:
            try:
                json_response: dict[any, any] = response.json()
            except JSONDecodeError:
                raise JSONDecodeError(
                    "There was a problem deserializing the request response in 'list_pokemon_generation'.")
            generation_name, pokemon_list = self.set_values_dict(json_response, generation_number, 'pokemon_species')
            pokemons_of_generation.setdefault(generation_name, pokemon_list)

        return pokemons_of_generation
    # def process(self, case) -> None:
