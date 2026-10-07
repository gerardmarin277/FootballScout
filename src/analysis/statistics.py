from __future__ import annotations
from typing import Dict, Any
import pandas as pd
from sqlalchemy.orm import Session
from src.database.repositories import PlayerRepository


class AnalyticsEngine:

    def __init__(self, db: Session):
        self.repo = PlayerRepository(db)

    def get_players_dataframe(self) -> pd.DataFrame:
        players = self.repo.get_all(limit=1000)
        data = []
        for p in players:
            row = {
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "nationality": p.nationality,
                "position": p.position.code if p.position else "N/A",
                "team": p.team.name if p.team else "Free",
                "market_value": p.market_value,
            }

            if p.statistics:
                s = p.statistics
                row.update({
                    "pace": s.pace,
                    "acceleration": s.acceleration,
                    "stamina": s.stamina,
                    "strength": s.strength,
                    "dribbling": s.dribbling,
                    "passing": s.passing,
                    "crossing": s.crossing,
                    "shooting": s.shooting,
                    "tackling": s.tackling,
                    "positioning": s.positioning,
                    "vision": s.vision,
                    "work_rate": s.work_rate,
                })

            data.append(row)
        return pd.DataFrame(data)

    def get_summary_stats(self) -> Dict[str, Any]:
        df = self.get_players_dataframe()

        if df.empty:
            return {}

        return {
            "total_players": int(len(df)),
            "avg_age": round(float(df["age"].mean()), 1),
            "avg_market_value": round(float(df["market_value"].mean()), 2),
            "top_value_player": df.loc[df["market_value"].idxmax()]["name"] if "market_value" in df else "N/A",
            "avg_pace": round(float(df["pace"].mean()), 1) if "pace" in df else 0.0,
            "avg_passing": round(float(df["passing"].mean()), 1) if "passing" in df else 0.0,
        }