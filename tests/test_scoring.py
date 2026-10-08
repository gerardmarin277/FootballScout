from src.scouting.scoring import ScoringEngine
from src.scouting.tactical_profile import TACTICAL_PROFILES


def test_calculate_compatibility(sample_data):
    player = sample_data["player1"]
    profile_winger = TACTICAL_PROFILES["RW_INVERTED"]  # Perfil definido en la V2

    scores = ScoringEngine.calculate_compatibility(player, profile_winger)

    assert "overall" in scores
    assert 0 <= scores["overall"] <= 100
    assert scores["overall"] >= 70.0


def test_compatibility_without_stats(db_session, sample_data):
    from src.models import Player

    player_no_stats = Player(
        name="Sin Stats",
        age=18,
        nationality="Spain",
        position_id=sample_data["pos_lw"].id,
    )
    db_session.add(player_no_stats)
    db_session.commit()

    profile = TACTICAL_PROFILES["RW_INVERTED"]
    scores = ScoringEngine.calculate_compatibility(player_no_stats, profile)

    assert scores["overall"] == 0.0