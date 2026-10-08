# ⚽ FootballScout: Sistema de Scouting & Analítica de Jugadores

**FootballScout** es una aplicación backend y CLI en Python diseñada para el análisis táctico, scouting avanzado, comparación de futbolistas y visualización de métricas de rendimiento.

---

## 🚀 Características Principales

- **Arquitectura Relacional (SQLAlchemy ORM)**: Persistencia de datos limpia con SQLite y soporte para múltiples ligas, equipos, posiciones y atributos detallados.
- **Motor de Scouting Táctico**: Puntuación de compatibilidad ponderada según perfiles tácticos (ej. *Extremo Invertido*, *Mediocentro Regulador*, *Central Marcador*).
- **Informes & Comparador Side-by-Side**: Generación de *Scouting Reports* visuales en consola e interfaz de comparación directa de métricas entre dos jugadores.
- **Analítica & Gráficos**: Procesamiento de métricas de la base de datos con **Pandas** y exportación automática de gráficos PNG con **Matplotlib**.
- **Suite de Tests Automatizada**: Pruebas unitarias e integración con **Pytest** utilizando SQLite en memoria.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.12+
- **ORM & DB**: SQLAlchemy 2.0+, SQLite
- **Analítica**: Pandas, Matplotlib
- **Testing**: Pytest
- **Herramientas**: Git, Virtualenv

---

## 📁 Estructura del Proyecto

```text
FootballScout/
├── data/
│   └── raw/              # Archivos CSV para importación masiva
├── reports/              # Gráficos analíticos generados (PNG)
├── src/
│   ├── analysis/         # Módulos de analítica, comparador y gráficos
│   ├── cli/              # Interfaz de línea de comandos (Menus)
│   ├── database/         # Configuración de base de datos y Repositorios
│   ├── models/           # Modelos ORM (Player, Team, Position, Statistics)
│   └── scouting/         # Perfiles tácticos y motor de scoring
├── tests/                # Suite de tests con Pytest
├── main.py               # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias del proyecto
└── README.md