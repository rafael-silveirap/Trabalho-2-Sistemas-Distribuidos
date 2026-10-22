import pathlib
import sys
from flask import render_template

basedir = pathlib.Path(__file__).parent.resolve()
if str(basedir) not in sys.path:
    sys.path.insert(0, str(basedir))

import config
from models import Evento, Ingresso

connex_app = config.connex_app
connex_app.add_api(config.basedir / "swagger.yml")

flask_app = connex_app.app


@flask_app.route("/")
def index():
    """Renderiza o painel visual interativo do EventPass."""
    return render_template("index.html")


if __name__ == "__main__":
    print("=" * 70)
    print("🎟️ EventPass API - Sistema de Venda e Divulgação de Ingressos Online")
    print("Painel Web:   http://127.0.0.1:8000")
    print("Swagger UI:   http://127.0.0.1:8000/api/ui")
    print("=" * 70)
    connex_app.run(host="127.0.0.1", port=8000)
