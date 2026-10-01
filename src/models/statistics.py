from __future__ import annotations
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base


class PlayerStatistics(Base):
    __tablename__ = "player_statistics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), unique=True, nullable=False)

    # Físicos
    pace: Mapped[int] = mapped_column(Integer, default=50)
    acceleration: Mapped[int] = mapped_column(Integer, default=50)
    stamina: Mapped[int] = mapped_column(Integer, default=50)
    strength: Mapped[int] = mapped_column(Integer, default=50)

    # Técnicos
    dribbling: Mapped[int] = mapped_column(Integer, default=50)
    passing: Mapped[int] = mapped_column(Integer, default=50)
    crossing: Mapped[int] = mapped_column(Integer, default=50)
    shooting: Mapped[int] = mapped_column(Integer, default=50)

    # Defensivos
    tackling: Mapped[int] = mapped_column(Integer, default=50)
    positioning: Mapped[int] = mapped_column(Integer, default=50)

    # Mentales
    vision: Mapped[int] = mapped_column(Integer, default=50)
    work_rate: Mapped[int] = mapped_column(Integer, default=50)

    player: Mapped["Player"] = relationship("Player", back_populates="statistics")

    def __repr__(self) -> str:
        return f"<Statistics PlayerID={self.player_id}>"