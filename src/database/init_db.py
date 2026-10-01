from src.database.connection import Base, engine, SessionLocal
from src.models import Position, Team, Player, PlayerStatistics


def init_database():
    print("🔨 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Pre-poblar posiciones básicas si no existen
        if db.query(Position).count() == 0:
            positions = [
                Position(code="GK", name="Goalkeeper", category="Goalkeeper"),
                Position(code="CB", name="Centre Back", category="Defender"),
                Position(code="RB", name="Right Back", category="Defender"),
                Position(code="LB", name="Left Back", category="Defender"),
                Position(code="CM", name="Central Midfielder", category="Midfielder"),
                Position(code="RM", name="Right Midfielder", category="Midfielder"),
                Position(code="LM", name="Left Midfielder", category="Midfielder"),
                Position(code="RW", name="Right Winger", category="Attacker"),
                Position(code="LW", name="Left Winger", category="Attacker"),
                Position(code="ST", name="Striker", category="Attacker"),
            ]
            db.add_all(positions)
            db.commit()
            print("✅ Posiciones estándar creadas correctamente.")
        else:
            print("ℹ️ Las posiciones ya estaban inicializadas.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al inicializar la base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()