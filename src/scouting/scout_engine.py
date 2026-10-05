from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.repositories import PlayerRepository
from src.models import Player
from src.scouting.scoring import ScoringEngine
from src.scouting.tactical_profile import TacticalProfile, TACTICAL_PROFILES


@dataclass
class ScoutMatch:
    player: Player
    compatibility_score: float
    tactical_profile: TacticalProfile


class ScoutEngine:
    def __init__(self, db: Session):
        self.repo = PlayerRepository(db)

    def analyze_player(self, player_id: int, profile_code: str) -> Optional[ScoutMatch]:
        player = self.repo.get_by_id(player_id)
        profile = TACTICAL_PROFILES.get(profile_code)

        if not player or not profile:
            return None

        scores = ScoringEngine.calculate_compatibility(player, profile)
        return ScoutMatch(
            player=player,
            compatibility_score=scores["overall"],
            tactical_profile=profile,
        )

    def search_candidates(
        self,
        profile_code: str,
        max_age: Optional[int] = None,
        max_market_value: Optional[float] = None,
        min_compatibility: float = 0.0,
    ) -> List[ScoutMatch]:
        profile = TACTICAL_PROFILES.get(profile_code)
        if not profile:
            return []

        all_players = self.repo.get_all(limit=500)
        results: List[ScoutMatch] = []

        for p in all_players:
            # Filtro por posición base si aplica
            if p.position and p.position.code != profile.target_position:
                continue

            # Filtros adicionales
            if max_age and p.age > max_age:
                continue
            if max_market_value and p.market_value > max_market_value:
                continue

            scores = ScoringEngine.calculate_compatibility(p, profile)
            score = scores["overall"]

            if score >= min_compatibility:
                results.append(
                    ScoutMatch(
                        player=p,
                        compatibility_score=score,
                        tactical_profile=profile,
                    )
                )

        # Ordenar de mayor a menor compatibilidad
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        return results