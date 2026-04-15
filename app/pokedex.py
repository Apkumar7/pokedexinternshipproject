from typing import Any, Callable, Dict, Optional

from app.pokeapi import get_pokemon_data, get_random_pokemon
from app.pokemon import Pokemon


class Pokedex:
    def __init__(
        self,
        data_fetcher: Callable[[Any], Dict[str, Any]] = get_pokemon_data,
        random_fetcher: Callable[[], Dict[str, Any]] = get_random_pokemon,
    ):
        self._data_fetcher = data_fetcher
        self._random_fetcher = random_fetcher

    def search(self, name_or_id: Any) -> Pokemon:
        pokemon_data = self._data_fetcher(name_or_id)
        return Pokemon.from_api_data(pokemon_data)

    def search_by_name(self, name: str) -> Pokemon:
        return self.search(name)

    def search_by_id(self, pokemon_id: int) -> Pokemon:
        return self.search(pokemon_id)

    def random_pokemon(self) -> Pokemon:
        pokemon_data = self._random_fetcher()
        return Pokemon.from_api_data(pokemon_data)
