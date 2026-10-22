from config import db
from flask import abort, make_response
from models import Person, people_schema, person_schema


def read_all():
    """Retorna todas as pessoas do banco de dados serializadas via Marshmallow."""
    people = Person.query.all()
    return people_schema.dump(people)


def create(person):
    """Cria uma nova pessoa no banco de dados SQLite."""
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")


def read_one(lname):
    """Busca uma pessoa pelo sobrenome no banco de dados."""
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")


def update(lname, person):
    """Atualiza o primeiro nome de uma pessoa no banco de dados."""
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person)
    else:
        abort(404, f"Person with last name {lname} not found")


def delete(lname):
    """Remove uma pessoa do banco de dados."""
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
