from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


class ChartGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_age_distribution(self, df: pd.DataFrame) -> str:
        if df.empty or "age" not in df:
            return ""

        plt.figure(figsize=(8, 5))
        plt.hist(df["age"], bins=8, color="#1f77b4", edgecolor="black", alpha=0.7)
        plt.title("Distribución de Edad de Jugadores", fontsize=14, fontweight="bold")
        plt.xlabel("Edad")
        plt.ylabel("Número de Jugadores")
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        output_path = self.output_dir / "age_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return str(output_path)

    def generate_pace_vs_age(self, df: pd.DataFrame) -> str:
        if df.empty or "pace" not in df or "age" not in df:
            return ""

        plt.figure(figsize=(8, 5))
        plt.scatter(df["age"], df["pace"], color="#d62728", s=80, alpha=0.8, edgecolors="black")
        plt.title("Relación: Ritmo vs Edad", fontsize=14, fontweight="bold")
        plt.xlabel("Edad")
        plt.ylabel("Ritmo (Pace)")
        plt.grid(True, linestyle="--", alpha=0.5)

        output_path = self.output_dir / "pace_vs_age.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return str(output_path)