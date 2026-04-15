import unittest

from app.pokemon import Pokemon


class TestPokemon(unittest.TestCase):
    def setUp(self):
        self.sample_api_data = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "types": [{"type": {"name": "electric"}}],
            "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}],
            "stats": [
                {"stat": {"name": "hp"}, "base_stat": 35},
                {"stat": {"name": "attack"}, "base_stat": 55},
            ],
            "sprites": {"front_default": "https://example.com/pikachu.png"},
            "moves": [{"move": {"name": "thunder-shock"}}, {"move": {"name": "quick-attack"}}],
        }

    def test_from_api_data_creates_pokemon(self):
        pokemon = Pokemon.from_api_data(self.sample_api_data)

        self.assertEqual(pokemon.id, 25)
        self.assertEqual(pokemon.name, "pikachu")
        self.assertEqual(pokemon.height, 4)
        self.assertEqual(pokemon.weight, 60)
        self.assertEqual(pokemon.types, ["electric"])
        self.assertEqual(pokemon.abilities, ["static", "lightning-rod"])
        self.assertEqual(pokemon.stats["hp"], 35)
        self.assertEqual(pokemon.sprite_url, "https://example.com/pikachu.png")
        self.assertEqual(pokemon.moves, ["thunder-shock", "quick-attack"])

    def test_to_dict_returns_dict_copy(self):
        pokemon = Pokemon.from_api_data(self.sample_api_data)
        data = pokemon.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "pikachu")
        self.assertEqual(data["types"], ["electric"])
        self.assertEqual(data["stats"]["attack"], 55)


if __name__ == "__main__":
    unittest.main()
