from __future__ import annotations
from typing import Optional
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)
    market_value: Mapped[float] = mapped_column(Float, default=0.0)  # En millones de €

    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"), nullable=True)

    # Relaciones
    position: Mapped["Position"] = relationship("Position", back_populates="players")
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")
    statistics: Mapped[Optional["PlayerStatistics"]] = relationship(
        "PlayerStatistics", back_populates="player", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Player {self.name} ({self.age}yo) - {self.position.code if self.position else 'N/A'}>"