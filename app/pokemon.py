from __future__ import annotations

from typing import Any, Dict, List, Optional


class Pokemon:
    def __init__(
        self,
        id: int,
        name: str,
        height: int,
        weight: int,
        types: List[str],
        abilities: List[str],
        stats: Dict[str, int],
        sprite_url: Optional[str] = None,
        moves: Optional[List[str]] = None,
        raw: Optional[Dict[str, Any]] = None,
    ):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.abilities = abilities
        self.stats = stats
        self.sprite_url = sprite_url
        self.moves = moves or []
        self.raw = raw or {}

    @classmethod
    def from_api_data(cls, data: Dict[str, Any]) -> "Pokemon":
        return cls(
            id=data.get("id", 0),
            name=data.get("name", ""),
            height=data.get("height", 0),
            weight=data.get("weight", 0),
            types=[type_info["type"]["name"] for type_info in data.get("types", [])],
            abilities=[ability_info["ability"]["name"] for ability_info in data.get("abilities", [])],
            stats={stat_info["stat"]["name"]: stat_info["base_stat"] for stat_info in data.get("stats", [])},
            sprite_url=data.get("sprites", {}).get("front_default"),
            moves=[move_info["move"]["name"] for move_info in data.get("moves", [])][:10],
            raw=data,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "types": list(self.types),
            "abilities": list(self.abilities),
            "stats": dict(self.stats),
            "sprite_url": self.sprite_url,
            "moves": list(self.moves),
            "raw": self.raw,
        }

    def __repr__(self) -> str:
        return f"Pokemon(id={self.id}, name={self.name!r})"
