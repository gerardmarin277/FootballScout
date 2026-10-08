import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.connection import Base
from src.models import Player, Position, PlayerStatistics, Team


@pytest.fixture(scope="function")
def db_session():
    """Crea una base de datos SQLite efímera en memoria para cada test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_data(db_session):
    """Pobla la base de datos con una muestra controlada de prueba."""
    pos_lw = Position(code="LW", name="Left Winger", category="DEL")
    pos_cm = Position(code="CM", name="Central Midfielder", category="MED")
    team_a = Team(name="FC Barcelona", country="Spain", league="LaLiga")

    db_session.add_all([pos_lw, pos_cm, team_a])
    db_session.commit()

    player1 = Player(
        name="Jugador A",
        age=20,
        nationality="España",
        market_value=50.0,
        position_id=pos_lw.id,
        team_id=team_a.id,
    )
    db_session.add(player1)
    db_session.commit()

    stats1 = PlayerStatistics(
        player_id=player1.id,
        pace=88,
        acceleration=90,
        stamina=75,
        strength=60,
        dribbling=85,
        passing=78,
        crossing=80,
        shooting=72,
        tackling=40,
        positioning=70,
        vision=80,
        work_rate=80,
    )
    db_session.add(stats1)
    db_session.commit()

    return {"player1": player1, "pos_lw": pos_lw, "team_a": team_a}