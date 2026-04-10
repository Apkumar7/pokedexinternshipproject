import base64
import os
import random
import requests

POKEAPI_BASE_URL = os.environ.get("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2")
POKEAPI_KEY = os.environ.get("POKEAPI_KEY")


def _build_headers():
    headers = {
        "Accept": "application/json",
    }
    if POKEAPI_KEY:
        headers["X-API-Key"] = POKEAPI_KEY
    return headers


def _raise_for_response(response):
    if response.status_code == 404:
        raise ValueError("Pokemon not found. Please check the name or ID.")
    response.raise_for_status()


def get_pokemon_data(name_or_id):
    """Retrieve Pokemon data from PokeAPI by name or numeric ID."""
    if name_or_id is None or name_or_id == "":
        raise ValueError("A Pokemon name or ID is required.")

    identifier = str(name_or_id).strip().lower()
    url = f"{POKEAPI_BASE_URL}/pokemon/{identifier}"
    response = requests.get(url, headers=_build_headers(), timeout=10)
    _raise_for_response(response)
    data = response.json()

    types = [type_info["type"]["name"] for type_info in data.get("types", [])]
    abilities = [ability_info["ability"]["name"] for ability_info in data.get("abilities", [])]
    stats = {stat_info["stat"]["name"]: stat_info["base_stat"] for stat_info in data.get("stats", [])}
    sprites = data.get("sprites", {})
    sprite_url = sprites.get("front_default")

    move_list = [move_info["move"]["name"] for move_info in data.get("moves", [])]
    moves = move_list[:10]

    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "types": types,
        "abilities": abilities,
        "stats": stats,
        "sprite_url": sprite_url,
        "moves": moves,
        "raw": data,
    }


def _get_pokemon_count():
    url = f"{POKEAPI_BASE_URL}/pokemon?limit=1"
    response = requests.get(url, headers=_build_headers(), timeout=10)
    _raise_for_response(response)
    return response.json().get("count", 1010)


def get_random_pokemon():
    """Retrieve a random Pokemon from the API."""
    count = _get_pokemon_count()
    for _ in range(5):
        random_id = random.randint(1, count)
        try:
            return get_pokemon_data(random_id)
        except ValueError:
            continue
    raise RuntimeError("Unable to retrieve a random Pokemon after several attempts.")
