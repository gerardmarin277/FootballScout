from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from src.models import Player, PlayerStatistics, Position, Team

class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_by_id(self, player_id: int) -> Optional[Player]:
        return (
            self.db.query(Player)
            .options(joinedload(Player.position), joinedload(Player.team), joinedload(Player.statistics))
            .filter(Player.id == player_id)
            .first()
        )

    def get_all(self, limit: int = 100) -> List[Player]:
        return (
            self.db.query(Player)
            .options(joinedload(Player.position), joinedload(Player.team), joinedload(Player.statistics))
            .limit(limit)
            .all()
        )

    def create(self, player: Player) -> Player:
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player

    def get_or_create_team(self, team_name: str, country: str = "Unknown", league: str = "Unknown") -> Team:
        team = self.db.query(Team).filter(Team.name == team_name).first()
        if not team:
            team = Team(name=team_name, country=country, league=league)
            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        return team

    def get_position_by_code(self, code: str) -> Optional[Position]:
        return self.db.query(Position).filter(Position.code == code).first()