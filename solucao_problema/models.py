from datetime import datetime, timezone
from marshmallow import fields, validate
from config import db, ma


class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    data_hora = db.Column(db.String(50), nullable=False)
    local = db.Column(db.String(150), nullable=False)
    preco_base = db.Column(db.Float, nullable=False)
    capacidade_total = db.Column(db.Integer, nullable=False)
    ingressos_disponiveis = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="ATIVO", nullable=False)
    criado_em = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relacionamento 1 para N com os ingressos emitidos
    ingressos = db.relationship(
        "Ingresso",
        backref="evento",
        cascade="all, delete-orphan",
        lazy=True,
    )


class Ingresso(db.Model):
    __tablename__ = "ingresso"

    id = db.Column(db.Integer, primary_key=True)
    codigo_bilhete = db.Column(db.String(36), unique=True, nullable=False)
    evento_id = db.Column(db.Integer, db.ForeignKey("evento.id"), nullable=False)
    comprador_nome = db.Column(db.String(100), nullable=False)
    comprador_email = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), default="INTEIRA", nullable=False)  # INTEIRA, MEIA, VIP
    valor_pago = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="CONFIRMADO", nullable=False)  # CONFIRMADO, CANCELADO
    data_compra = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class IngressoSchema(ma.SQLAlchemyAutoSchema):
    evento_titulo = fields.Method("get_evento_titulo")

    class Meta:
        model = Ingresso
        load_instance = True
        sqla_session = db.session
        include_fk = True

    def get_evento_titulo(self, obj):
        return obj.evento.titulo if obj.evento else "Evento Indisponível"


class EventoSchema(ma.SQLAlchemyAutoSchema):
    ingressos_vendidos = fields.Method("get_ingressos_vendidos")

    class Meta:
        model = Evento
        load_instance = True
        sqla_session = db.session

    def get_ingressos_vendidos(self, obj):
        return obj.capacidade_total - obj.ingressos_disponiveis


# Instâncias para serialização unitária e em listas
evento_schema = EventoSchema()
eventos_schema = EventoSchema(many=True)

ingresso_schema = IngressoSchema()
ingressos_schema = IngressoSchema(many=True)
