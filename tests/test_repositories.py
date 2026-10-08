from src.database.repositories import PlayerRepository
from src.models import Player


def test_get_all_players(db_session, sample_data):
    repo = PlayerRepository(db_session)
    players = repo.get_all()

    assert len(players) == 1
    assert players[0].name == "Jugador A"


def test_search_by_position(db_session, sample_data):
    repo = PlayerRepository(db_session)
    players = repo.get_all()
    wingers = [p for p in players if p.position and p.position.code == "LW"]
    strikers = [p for p in players if p.position and p.position.code == "ST"]

    assert len(wingers) == 1
    assert len(strikers) == 0


def test_create_player(db_session, sample_data):
    repo = PlayerRepository(db_session)
    new_player = Player(
        name="Nuevo Fichaje",
        age=22,
        nationality="Brasil",
        market_value=30.0,
        position_id=sample_data["pos_lw"].id,
    )
    # Usa create() en lugar de save()
    saved_player = repo.create(new_player)

    assert saved_player.id is not None
    assert saved_player.name == "Nuevo Fichaje"