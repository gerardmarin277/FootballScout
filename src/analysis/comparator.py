from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from src.models import Player
from src.scouting.scoring import ScoringEngine
from src.scouting.tactical_profile import TACTICAL_PROFILES

@dataclass
class ComparisonResult:
    player_a: Player
    player_b: Player
    stat_diffs: Dict[str, int]
    profile_scores_a: Dict[str, float]
    profile_scores_b: Dict[str, float]


class PlayerComparator:

    @staticmethod
    def compare(player_a: Player, player_b: Player) -> ComparisonResult:
        stats_a = player_a.statistics
        stats_b = player_b.statistics

        stat_keys = [
            "pace", "acceleration", "stamina", "strength",
            "dribbling", "passing", "crossing", "shooting",
            "tackling", "positioning", "vision", "work_rate"
        ]

        stat_diffs: Dict[str, int] = {}
        for key in stat_keys:
            val_a = getattr(stats_a, key, 0) if stats_a else 0
            val_b = getattr(stats_b, key, 0) if stats_b else 0
            stat_diffs[key] = val_a - val_b


        profile_scores_a = {}
        profile_scores_b = {}
        for code, profile in TACTICAL_PROFILES.items():
            profile_scores_a[code] = ScoringEngine.calculate_compatibility(player_a, profile)["overall"]
            profile_scores_b[code] = ScoringEngine.calculate_compatibility(player_b, profile)["overall"]


        return ComparisonResult(
            player_a=player_a,
            player_b=player_b,
            stat_diffs=stat_diffs,
            profile_scores_a=profile_scores_a,
            profile_scores_b=profile_scores_b,
        )
