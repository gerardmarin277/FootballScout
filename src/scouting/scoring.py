from __future__ import annotations
from typing import Dict
from src.models import Player
from src.scouting.tactical_profile import TacticalProfile

class ScoringEngine:
    @staticmethod
    def calculate_compatibility(player: PLayer, profile: TacticalProfile) -> Dict[str, float]:
        """Calcula el porcentaje de compatibilidad de un jugador con un perfil táctico."""
        if not player.statistics:
            return {"overall": 0.0}

        stats = player.statistics
        total_score = 0.0
        applied_weight = 0.0 

        for attr, weight in profile.weights.items():
            value = getattr(stats, attr, None)
            if value is not None:
                total_score += value * weight
                applied_weight += weight


        final_score = (total_score / applied_weight) if applied_weight > 0 else 0.0


        return {
            "overall": round(final_score, 1),
        }

    