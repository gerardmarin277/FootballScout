from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TacticalProfile:
    name: str
    code: str
    target_position: str  # Ej: RW, CM, CB
    description: str
    # Diccionario con el atributo y su peso % (la suma debe dar 1.0)
    weights: Dict[str, float] = field(default_factory=dict)


# Perfiles tácticos predefinidos
TACTICAL_PROFILES = {
    "RW_INVERTED": TacticalProfile(
        name="Inverted Winger (RW)",
        code="RW_INVERTED",
        target_position="RW",
        description="Extremo a pierna cambiada que busca recortar hacia dentro, asociarse y rematar.",
        weights={
            "dribbling": 0.20,
            "pace": 0.15,
            "acceleration": 0.15,
            "passing": 0.15,
            "vision": 0.15,
            "shooting": 0.10,
            "stamina": 0.10,
        },
    ),
    "RW_TRADITIONAL": TacticalProfile(
        name="Traditional Winger (RW)",
        code="RW_TRADITIONAL",
        target_position="RW",
        description="Extremo de banda clásico orientado a llegar a línea de fondo y poner centros.",
        weights={
            "pace": 0.25,
            "acceleration": 0.20,
            "dribbling": 0.20,
            "crossing": 0.20,
            "stamina": 0.15,
        },
    ),
    "CM_BOX_TO_BOX": TacticalProfile(
        name="Box-to-Box Midfielder (CM)",
        code="CM_BOX_TO_BOX",
        target_position="CM",
        description="Centrocampista todoterreno con gran despliegue físico, trabajo defensivo y llegada.",
        weights={
            "stamina": 0.20,
            "work_rate": 0.15,
            "passing": 0.15,
            "tackling": 0.15,
            "positioning": 0.15,
            "strength": 0.10,
            "vision": 0.10,
        },
    ),
    "ST_POACHER": TacticalProfile(
        name="Poacher / Goalscorer (ST)",
        code="ST_POACHER",
        target_position="ST",
        description="Delantero de área centrado en el remate, velocidad corta y desmarque.",
        weights={
            "shooting": 0.30,
            "acceleration": 0.20,
            "positioning": 0.20,
            "pace": 0.15,
            "strength": 0.15,
        },
    ),
}