import unittest

from app.pokeapi import get_pokemon_data, get_random_pokemon


class TestPokeAPI(unittest.TestCase):
    def test_get_pokemon_data_valid_name(self):
        pikachu = get_pokemon_data("pikachu")
        self.assertEqual(pikachu["name"], "pikachu")
        self.assertEqual(pikachu["id"], 25)
        self.assertIn("electric", pikachu["types"])
        self.assertIsInstance(pikachu["abilities"], list)
        self.assertIsInstance(pikachu["stats"], dict)

    def test_get_pokemon_data_valid_id(self):
        bulbasaur = get_pokemon_data(1)
        self.assertEqual(bulbasaur["name"], "bulbasaur")
        self.assertEqual(bulbasaur["id"], 1)

    def test_get_pokemon_data_invalid(self):
        with self.assertRaises(ValueError):
            get_pokemon_data("not-a-pokemon")

    def test_get_random_pokemon(self):
        random_pokemon = get_random_pokemon()
        self.assertIsInstance(random_pokemon, dict)
        self.assertIn("name", random_pokemon)
        self.assertIn("id", random_pokemon)


if __name__ == "__main__":
    unittest.main()
