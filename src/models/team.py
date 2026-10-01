from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    league: Mapped[str] = mapped_column(String(50), nullable=False)

    players: Mapped[list["Player"]] = relationship("Player", back_populates="team")

    def __repr__(self) -> str:
        return f"<Team {self.name} ({self.league})>"