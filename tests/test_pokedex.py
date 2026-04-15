import unittest
from unittest.mock import Mock

from app.pokedex import Pokedex
from app.pokemon import Pokemon


class TestPokedex(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "id": 1,
            "name": "bulbasaur",
            "height": 7,
            "weight": 69,
            "types": [{"type": {"name": "grass"}}, {"type": {"name": "poison"}}],
            "abilities": [{"ability": {"name": "overgrow"}}],
            "stats": [{"stat": {"name": "hp"}, "base_stat": 45}],
            "sprites": {"front_default": "https://example.com/bulbasaur.png"},
            "moves": [{"move": {"name": "tackle"}}],
        }
        self.data_fetcher = Mock(return_value=self.sample_data)
        self.random_fetcher = Mock(return_value=self.sample_data)
        self.pokedex = Pokedex(data_fetcher=self.data_fetcher, random_fetcher=self.random_fetcher)

    def test_search_returns_pokemon_instance(self):
        pokemon = self.pokedex.search("bulbasaur")

        self.data_fetcher.assert_called_once_with("bulbasaur")
        self.assertIsInstance(pokemon, Pokemon)
        self.assertEqual(pokemon.name, "bulbasaur")

    def test_search_by_id_uses_data_fetcher(self):
        pokemon = self.pokedex.search_by_id(1)

        self.data_fetcher.assert_called_once_with(1)
        self.assertEqual(pokemon.id, 1)

    def test_random_pokemon_returns_pokemon(self):
        pokemon = self.pokedex.random_pokemon()

        self.random_fetcher.assert_called_once()
        self.assertEqual(pokemon.name, "bulbasaur")


if __name__ == "__main__":
    unittest.main()
