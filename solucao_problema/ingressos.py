import uuid
from config import db
from flask import abort, make_response
from models import Evento, Ingresso, ingresso_schema, ingressos_schema


def read_all(email=None):
    """
    Lista todos os ingressos emitidos com filtro opcional por email do comprador.
    """
    query = Ingresso.query
    if email:
        query = query.filter(Ingresso.comprador_email.ilike(f"%{email}%"))
    ingressos = query.order_by(Ingresso.data_compra.desc()).all()
    return ingressos_schema.dump(ingressos)


def read_one(codigo_bilhete):
    """
    Consulta os detalhes de um bilhete pelo seu código único.
    """
    ingresso = Ingresso.query.filter(Ingresso.codigo_bilhete == codigo_bilhete.upper()).one_or_none()
    if ingresso is not None:
        return ingresso_schema.dump(ingresso)
    else:
        abort(404, f"Bilhete '{codigo_bilhete}' não encontrado")


def comprar(compra):
    """
    Efetua a compra de um ingresso para um evento específico.
    Aplica regras de negócio:
    - Verificação de vagas (ingressos_disponiveis > 0).
    - Cálculo de valor:
        * INTEIRA: 100% do preço base
        * MEIA: 50% do preço base
        * VIP: 150% do preço base
    - Decremento automático de estoque de ingressos.
    - Se vagas chegarem a zero, marca o evento como ESGOTADO.
    - Geração de código de bilhete alfanumérico único.
    """
    evento_id = compra.get("evento_id")
    comprador_nome = compra.get("comprador_nome", "").strip()
    comprador_email = compra.get("comprador_email", "").strip()
    tipo = compra.get("tipo", "INTEIRA").upper().strip()

    if not evento_id or not comprador_nome or not comprador_email:
        abort(400, "Os campos 'evento_id', 'comprador_nome' e 'comprador_email' são obrigatórios")

    if tipo not in ["INTEIRA", "MEIA", "VIP"]:
        abort(400, "Tipo de ingresso inválido. Escolha entre: INTEIRA, MEIA ou VIP")

    evento = Evento.query.filter(Evento.id == evento_id).one_or_none()
    if not evento:
        abort(404, f"Evento com ID {evento_id} não encontrado")

    if evento.ingressos_disponiveis <= 0 or evento.status == "ESGOTADO":
        abort(400, f"Ingressos esgotados para o evento '{evento.titulo}'")

    # Cálculo da precificação conforme regra de negócio
    if tipo == "MEIA":
        valor_pago = round(evento.preco_base * 0.5, 2)
    elif tipo == "VIP":
        valor_pago = round(evento.preco_base * 1.5, 2)
    else:
        valor_pago = round(evento.preco_base, 2)

    # Geração do código único do bilhete
    codigo_bilhete = f"TKT-{uuid.uuid4().hex[:8].upper()}"

    # Decremento de disponibilidade
    evento.ingressos_disponiveis -= 1
    if evento.ingressos_disponiveis == 0:
        evento.status = "ESGOTADO"

    novo_ingresso = Ingresso(
        codigo_bilhete=codigo_bilhete,
        evento_id=evento.id,
        comprador_nome=comprador_nome,
        comprador_email=comprador_email,
        tipo=tipo,
        valor_pago=valor_pago,
        status="CONFIRMADO",
    )

    db.session.add(novo_ingresso)
    db.session.commit()

    return ingresso_schema.dump(novo_ingresso), 201


def cancelar(codigo_bilhete):
    """
    Cancela um ingresso existente e devolve a vaga para a disponibilidade do evento.
    """
    ingresso = Ingresso.query.filter(Ingresso.codigo_bilhete == codigo_bilhete.upper()).one_or_none()
    if not ingresso:
        abort(404, f"Bilhete '{codigo_bilhete}' não encontrado")

    if ingresso.status == "CANCELADO":
        abort(400, f"O bilhete '{codigo_bilhete}' já se encontra cancelado")

    ingresso.status = "CANCELADO"

    # Restitui a vaga ao evento correspondente
    evento = ingresso.evento
    if evento:
        evento.ingressos_disponiveis += 1
        if evento.status == "ESGOTADO":
            evento.status = "ATIVO"

    db.session.commit()

    return {
        "mensagem": f"Bilhete {codigo_bilhete} cancelado com sucesso. Vaga restituída ao evento.",
        "codigo_bilhete": codigo_bilhete,
        "valor_estornado": ingresso.valor_pago,
        "status": "CANCELADO",
    }, 200
