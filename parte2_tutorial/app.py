import pathlib
import sys
from flask import render_template

basedir = pathlib.Path(__file__).parent.resolve()
if str(basedir) not in sys.path:
    sys.path.insert(0, str(basedir))

import config
from models import Person

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)


if __name__ == "__main__":
    print("Iniciando API Parte 2 em http://127.0.0.1:8000 (Swagger UI: http://127.0.0.1:8000/api/ui)")
    app.run(host="127.0.0.1", port=8000)
