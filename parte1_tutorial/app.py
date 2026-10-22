import pathlib
import sys
import connexion
from flask import render_template

basedir = pathlib.Path(__file__).parent.resolve()
if str(basedir) not in sys.path:
    sys.path.insert(0, str(basedir))

connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app.add_api("swagger.yml")

app = connex_app.app


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    print("Iniciando API Parte 1 em http://127.0.0.1:8000 (Swagger UI: http://127.0.0.1:8000/api/ui)")
    connex_app.run(host="127.0.0.1", port=8000)
