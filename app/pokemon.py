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
        # Robust parsing to handle potential API response variations
        types = []
        if isinstance(data.get("types"), list):
            types = [type_info.get("type", {}).get("name", "") for type_info in data.get("types", []) if isinstance(type_info, dict)]

        abilities = []
        if isinstance(data.get("abilities"), list):
            abilities = [ability_info.get("ability", {}).get("name", "") for ability_info in data.get("abilities", []) if isinstance(ability_info, dict)]

        stats = {}
        if isinstance(data.get("stats"), list):
            stats = {stat_info.get("stat", {}).get("name", ""): stat_info.get("base_stat", 0) for stat_info in data.get("stats", []) if isinstance(stat_info, dict)}

        moves = []
        if isinstance(data.get("moves"), list):
            moves = [move_info.get("move", {}).get("name", "") for move_info in data.get("moves", []) if isinstance(move_info, dict)][:10]

        sprites = data.get("sprites", {}) if isinstance(data.get("sprites"), dict) else {}
        sprite_url = sprites.get("front_default") if isinstance(sprites, dict) else None

        return cls(
            id=data.get("id", 0) if isinstance(data.get("id"), int) else 0,
            name=data.get("name", "") if isinstance(data.get("name"), str) else "",
            height=data.get("height", 0) if isinstance(data.get("height"), int) else 0,
            weight=data.get("weight", 0) if isinstance(data.get("weight"), int) else 0,
            types=types,
            abilities=abilities,
            stats=stats,
            sprite_url=sprite_url,
            moves=moves,
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
