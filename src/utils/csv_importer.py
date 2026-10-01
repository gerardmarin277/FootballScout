from __future__ import annotations
import csv
from pathlib import Path
from src.database.connection import SessionLocal
from src.database.repositories import PlayerRepository
from src.models import Player, PlayerStatistics


def import_players_from_csv(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"❌ El archivo no existe: {file_path}")
        return 0

    db = SessionLocal()
    repo = PlayerRepository(db)
    imported_count = 0

    try:
        with open(path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Buscar posición por código
                position = repo.get_position_by_code(row["position"])
                if not position:
                    print(f"⚠️ Posición no encontrada para {row['name']}: {row['position']}")
                    continue

                # Buscar o crear equipo
                team = repo.get_or_create_team(row["team"]) if row.get("team") else None

                # Crear jugador
                player = Player(
                    name=row["name"],
                    age=int(row["age"]),
                    nationality=row["nationality"],
                    market_value=float(row.get("market_value", 0.0)),
                    position_id=position.id,
                    team_id=team.id if team else None,
                )

                # Asignar estadísticas
                stats = PlayerStatistics(
                    pace=int(row["pace"]),
                    acceleration=int(row["acceleration"]),
                    stamina=int(row["stamina"]),
                    strength=int(row["strength"]),
                    dribbling=int(row["dribbling"]),
                    passing=int(row["passing"]),
                    crossing=int(row["crossing"]),
                    shooting=int(row["shooting"]),
                    tackling=int(row["tackling"]),
                    positioning=int(row["positioning"]),
                    vision=int(row["vision"]),
                    work_rate=int(row["work_rate"]),
                )
                player.statistics = stats

                repo.create(player)
                imported_count += 1

        print(f"✅ Se han importado {imported_count} jugadores con éxito.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante la importación: {e}")
    finally:
        db.close()

    return imported_count


if __name__ == "__main__":
    import_players_from_csv("data/raw/players.csv")