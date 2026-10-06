from __future__ import annotations
from typing import List, Tuple
from src.models import Player
from src.scouting.scoring import ScoringEngine
from src.scouting.tactical_profile import TacticalProfile


class ReportGenerator:
    @staticmethod
    def generate_scouting_report(player: Player, profile: TacticalProfile) -> str:
        s = player.statistics
        if not s:
            return "❌ El jugador no posee estadísticas registradas."

        scores = ScoringEngine.calculate_compatibility(player, profile)
        compatibility = scores["overall"]

        # Identificar fortalezas (>= 80) y debilidades (< 65)
        attr_map = {
            "Ritmo": s.pace,
            "Aceleración": s.acceleration,
            "Resistencia": s.stamina,
            "Fuerza": s.strength,
            "Regate": s.dribbling,
            "Pase": s.passing,
            "Centros": s.crossing,
            "Tiro": s.shooting,
            "Entradas": s.tackling,
            "Posicionamiento": s.positioning,
            "Visión": s.vision,
            "Trabajo": s.work_rate,
        }

        strengths = [f"+ {k} ({v})" for k, v in attr_map.items() if v >= 80]
        weaknesses = [f"- {k} ({v})" for k, v in attr_map.items() if v < 65]

        report = []
        report.append("=" * 55)
        report.append("                  📋 SCOUTING REPORT                 ")
        report.append("=" * 55)
        report.append(f" JUGADOR:       {player.name} ({player.age} años)")
        report.append(f" EQUIPO:        {player.team.name if player.team else 'Libre'}")
        report.append(f" POSICIÓN:      {player.position.name} [{player.position.code}]")
        report.append(f" VALOR MERCADO: {player.market_value} M€")
        report.append("-" * 55)
        report.append(f" PERFIL TÁCTICO EVALUADO: {profile.name}")
        report.append(f" COMPATIBILIDAD TÁCTICA:  {compatibility}%")
        report.append("-" * 55)
        report.append(" 📊 ATRIBUTOS DESTACADOS")
        report.append(f"   FÍSICO:   Ritmo: {s.pace} | Acel: {s.acceleration} | Resis: {s.stamina} | Fuerza: {s.strength}")
        report.append(f"   TÉCNICA:  Regate: {s.dribbling} | Pase: {s.passing} | Centro: {s.crossing} | Tiro: {s.shooting}")
        report.append(f"   DEFENSA:  Entradas: {s.tackling} | Posicionamiento: {s.positioning}")
        report.append(f"   MENTAL:   Visión: {s.vision} | Trabajo: {s.work_rate}")
        report.append("-" * 55)
        report.append(" 💪 PUNTOS FUERTES:")
        if strengths:
            for st in strengths:
                report.append(f"   {st}")
        else:
            report.append("   - Ningún atributo superior a 80")

        report.append("\n ⚠️ ÁREAS DE MEJORA:")
        if weaknesses:
            for wk in weaknesses:
                report.append(f"   {wk}")
        else:
            report.append("   - Ninguna debilidad marcada (<65)")
        report.append("=" * 55)

        return "\n".join(report)