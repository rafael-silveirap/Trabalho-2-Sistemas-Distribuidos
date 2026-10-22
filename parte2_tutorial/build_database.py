"""
Script para inicializar e popular o banco de dados SQLite (people.db)
com os registros de exemplo do tutorial.
"""
import sys
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(basedir))

import config
from models import Person, db

PEOPLE = [
    {"fname": "Tooth", "lname": "Fairy"},
    {"fname": "Knecht", "lname": "Ruprecht"},
    {"fname": "Easter", "lname": "Bunny"},
]


def build_database():
    with config.app.app_context():
        db_path = config.basedir / "people.db"
        if db_path.exists():
            db_path.unlink()
            print(f"Banco anterior '{db_path.name}' removido para recriação limpa.")

        db.create_all()
        print("Tabela 'person' criada com sucesso via SQLAlchemy.")

        for person_data in PEOPLE:
            new_person = Person(
                fname=person_data["fname"],
                lname=person_data["lname"],
            )
            db.session.add(new_person)

        db.session.commit()
        print(f"Banco inicializado com {len(PEOPLE)} pessoas cadastradas.")


if __name__ == "__main__":
    build_database()
