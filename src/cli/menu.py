from __future__ import annotations
from src.database.connection import SessionLocal
from src.database.repositories import PlayerRepository

def print_header():
    print("=" * 50)
    print("           ⚽ FOOTBALLSCOUT - CLI V1          ")
    print("    Football Scouting & Player Analytics Platform ")
    print("=" * 50)

def list_players():
    db = SessionLocal()
    repo = PlayerRepository(db)
    players = repo.get_all()
    db.close()

    print("\n📋 JUGADORES EN LA BASE DE DATOS")
    print("-" * 65)
    print(f"{'ID':<4} | {'Nombre':<20} | {'Edad':<4} | {'Pos':<4} | {'Equipo':<18} | {'Valor (€M)'}")
    print("-" * 65)


    if not players:
        print("No hay jugadores en la base de datos.")
        return

    for p in players:
        team_name = p.team.name if p.team else "Libre"
        pos_code = p.position.code if p.position else "N/A"
        print(f"{p.id:<4} | {p.name:<20} | {p.age:<4} | {pos_code:<4} | {team_name:<18} | {p.market_value:<10.1f}")
    print("=" * 65)



def view_player_detail():
    player_id = input("\n🔍 Introduce el ID del jugador: ").strip()
    if not player_id.isdigit():
        print("❌ ID inválido. Por favor, introduce un número entero.")
        return

    db = SessionLocal()
    repo = PlayerRepository(db)
    p = repo.get_by_id(int(player_id))
    db.close()

    if not p:
        print(f"❌ No se encontró ningún jugador con ID {player_id}.")
        return

    print("\n" + "=" * 45)
    print(f"👤 FICHA TÉCNICA: {p.name.upper()}")
    print("=" * 45)
    print(f"Edad:         {p.age} años")
    print(f"Nacionalidad: {p.nationality}")
    print(f"Posición:     {p.position.name} ({p.position.code})")
    print(f"Equipo:       {p.team.name if p.team else 'Libre'}")
    print(f"Valor:        {p.market_value} M€")

    if p.statistics:
        s = p.statistics
        print("\n📊 ATRIBUTOS CLAVE (0-100)")
        print("-" * 45)
        print(f"Físicos:    Pace: {s.pace} | Accel: {s.acceleration} | Stamina: {s.stamina} | Strength: {s.strength}")
        print(f"Técnicos:   Dribbling: {s.dribbling} | Passing: {s.passing} | Crossing: {s.crossing} | Shooting: {s.shooting}")
        print(f"Defensivos: Tackling: {s.tackling} | Positioning: {s.positioning}")
        print(f"Mentales:   Vision: {s.vision} | Work Rate: {s.work_rate}")
    print("=" * 45)


def start_cli():
    while True:
        print_header()
        print("1. 📋 Listar todos los jugadores")
        print("2. 🔍 Ver detalle de un jugador")
        print("3. 📥 Importar jugadores desde CSV (data/raw/players.csv)")
        print("4. 🎯 Scouting por Perfil Táctico")
        print("5. ⚔️ Comparar 2 jugadores side-by-side")
        print("6. 📄 Generar Scouting Report completo")
        print("7. 📈 Analítica Global y Generación de Gráficos")
        print("0. 🚪 Salir")
        
        choice = input("\nSelecciona una opción: ").strip()

        if choice == "1":
            list_players()
        elif choice == "2":
            view_player_detail()
        elif choice == "3":
            from src.utils.csv_importer import import_players_from_csv
            import_players_from_csv("data/raw/players.csv")
        elif choice == "4":
            scouting_menu()
        elif choice == "5":
            compare_players_menu()
        elif choice == "6":
            generate_report_menu()
        elif choice == "7":
            analytics_menu()
        elif choice == "0":
            print("\n👋 ¡Hasta pronto scout!\n")
            break
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.\n")
        
        input("\nPresiona Enter para continuar...")


def scouting_menu():
    from src.scouting.scout_engine import ScoutEngine
    from src.scouting.tactical_profile import TACTICAL_PROFILES

    print("\n🎯 MÓDULO DE SCOUTING Y PROFILES TÁCTICOS")
    print("-" * 50)
    print("Perfiles disponibles:")
    for i, (code, profile) in enumerate(TACTICAL_PROFILES.items(), 1):
        print(f"  {i}. {profile.name} [{code}] - {profile.description}")

    p_choice = input("\nSelecciona un perfil (número): ").strip()
    keys = list(TACTICAL_PROFILES.keys())

    if not p_choice.isdigit() or int(p_choice) < 1 or int(p_choice) > len(keys):
        print("❌ Perfil inválido.")
        return

    selected_code = keys[int(p_choice) - 1]

    max_age_in = input("Edad máxima (deja en blanco para omitir): ").strip()
    max_age = int(max_age_in) if max_age_in.isdigit() else None

    db = SessionLocal()
    engine = ScoutEngine(db)
    matches = engine.search_candidates(selected_code, max_age=max_age)
    db.close()

    print("\n" + "=" * 60)
    print(f"🔎 RESULTADOS SCOUTING - PERFIL: {selected_code}")
    print("=" * 60)
    print(f"{'Ranking':<8} | {'Nombre':<20} | {'Edad':<5} | {'Compatibilidad'}")
    print("-" * 60)

    if not matches:
        print("No se encontraron candidatos que cumplan los criterios.")
        return

    for idx, match in enumerate(matches, 1):
        p = match.player
        print(f"#{idx:<7} | {p.name:<20} | {p.age:<5} | {match.compatibility_score}%")
    print("=" * 60)



def compare_players_menu():
    from src.analysis.comparator import PlayerComparator

    print("\n⚔️ COMPARADOR DE JUGADORES SIDE-BY-SIDE")
    print("-" * 50)
    id_a = input("Introduce el ID del primer jugador (Player A): ").strip()
    id_b = input("Introduce el ID del segundo jugador (Player B): ").strip()

    if not id_a.isdigit() or not id_b.isdigit():
        print("❌ IDs inválidos.")
        return

    db = SessionLocal()
    repo = PlayerRepository(db)
    p_a = repo.get_by_id(int(id_a))
    p_b = repo.get_by_id(int(id_b))
    db.close()

    if not p_a or not p_b:
        print("❌ Uno o ambos jugadores no existen.")
        return

    res = PlayerComparator.compare(p_a, p_b)

    print("\n" + "=" * 60)
    print(f"{'ATRIBUTO':<18} | {p_a.name[:15]:<15} | {p_b.name[:15]:<15} | {'DIFERENCIA'}")
    print("=" * 60)
    for stat, diff in res.stat_diffs.items():
        val_a = getattr(p_a.statistics, stat, 0)
        val_b = getattr(p_b.statistics, stat, 0)
        diff_str = f"+{diff}" if diff > 0 else f"{diff}"
        print(f"{stat.capitalize():<18} | {val_a:<15} | {val_b:<15} | {diff_str}")
    print("=" * 60)


def generate_report_menu():
    from src.analysis.reports import ReportGenerator
    from src.scouting.tactical_profile import TACTICAL_PROFILES

    player_id = input("\nIntroduce el ID del jugador para el informe: ").strip()
    if not player_id.isdigit():
        print("❌ ID no válido.")
        return

    db = SessionLocal()
    repo = PlayerRepository(db)
    player = repo.get_by_id(int(player_id))
    db.close()

    if not player:
        print("❌ Jugador no encontrado.")
        return

    print("\nSelecciona el Perfil Táctico para la evaluación:")
    for i, (code, profile) in enumerate(TACTICAL_PROFILES.items(), 1):
        print(f"  {i}. {profile.name}")

    p_choice = input("Opción: ").strip()
    keys = list(TACTICAL_PROFILES.keys())

    if not p_choice.isdigit() or int(p_choice) < 1 or int(p_choice) > len(keys):
        print("❌ Perfil inválido.")
        return

    selected_profile = TACTICAL_PROFILES[keys[int(p_choice) - 1]]
    report_text = ReportGenerator.generate_scouting_report(player, selected_profile)
    print("\n" + report_text)


def analytics_menu():
    from src.analysis.statistics import AnalyticsEngine
    from src.analysis.charts import ChartGenerator

    db = SessionLocal()
    engine = AnalyticsEngine(db)
    stats = engine.get_summary_stats()
    df = engine.get_players_dataframe()
    db.close()

    if not stats:
        print("❌ No hay suficientes datos para generar analítica.")
        return

    print("\n" + "=" * 50)
    print("           📈 ANALÍTICA GLOBAL DE LA BASE DE DATOS         ")
    print("=" * 50)
    print(f"Total Jugadores:       {stats['total_players']}")
    print(f"Edad Media:            {stats['avg_age']} años")
    print(f"Valor de Mercado M.:   {stats['avg_market_value']} M€")
    print(f"Jugador más Valioso:   {stats['top_value_player']}")
    print(f"Media Ritmo (Pace):    {stats['avg_pace']}")
    print(f"Media Pase (Passing):  {stats['avg_passing']}")
    print("=" * 50)

    gen_charts = input("\n¿Deseas generar los gráficos analíticos en /reports? (S/N): ").strip().upper()
    if gen_charts == "S":
        chart_gen = ChartGenerator()
        path1 = chart_gen.generate_age_distribution(df)
        path2 = chart_gen.generate_pace_vs_age(df)
        print(f"✅ Gráfico generado: {path1}")
        print(f"✅ Gráfico generado: {path2}")