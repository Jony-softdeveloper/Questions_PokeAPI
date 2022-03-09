"""Class reference for Pokemon."""
from typing import Optional

class Pokemon():
    """Model the basic features of a pokemon and some related with the
    functionality of this program.

    Attributes
    ----------
    id: int
    name: str
        Or species name of the pokemon. Alwasy in lowercase.
    egg_groups: Optional[dict[str, str]]
        Categories which determine with which Pokémon are able
        to interbreed.
    weight: Optional[float]
        Weight in kg.
    height: Optional[float]
        Height in m.
    """

    def __init__(self, id: int, name: str, weight: Optional[float] = None, 
                height: Optional[float] = None, egg_groups: Optional[dict[str, str]] = None) -> None:
        """Initialize the aspects of the pokemon.
        
        Parameters
        ----------
        id: int
        name: str
        egg_groups: Dict[str, str]

        Other Parameters
        ----------------
        weight: float
        height: float
        """
        self.id: int = id
        self.name: str = name
        self.height: Optional[float] = height
        self.weight: Optional[float] = weight
        self.egg_groups: Optional[dict[str, str]] = egg_groups

    def __str__(self) -> str:
        """Return the ID name of the pokemon."""
        return f'{self.id}. {self.name.title()}'

