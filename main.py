from src.cli.menu import start_cli
from src.database.init_db import init_database

if __name__ == "__main__":
    init_database()
    start_cli()