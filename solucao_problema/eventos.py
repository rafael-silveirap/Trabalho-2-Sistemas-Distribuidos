from config import db
from flask import abort, make_response
from models import Evento, evento_schema, eventos_schema


def read_all(categoria=None, status=None):
    """
    Retorna a lista de eventos com suporte a filtros opcionais por categoria e status.
    """
    query = Evento.query
    if categoria:
        query = query.filter(Evento.categoria.ilike(f"%{categoria}%"))
    if status:
        query = query.filter(Evento.status == status.upper())

    eventos = query.all()
    return eventos_schema.dump(eventos)


def read_one(evento_id):
    """
    Retorna os detalhes completos de um evento pelo seu ID.
    """
    evento = Evento.query.filter(Evento.id == evento_id).one_or_none()
    if evento is not None:
        return evento_schema.dump(evento)
    else:
        abort(404, f"Evento com ID {evento_id} não encontrado")


def create(evento):
    """
    Cadastra um novo evento com validações de unicidade de título e capacidade.
    """
    titulo = evento.get("titulo", "").strip()
    if not titulo:
        abort(400, "O campo 'titulo' é obrigatório")

    existing_evento = Evento.query.filter(Evento.titulo == titulo).one_or_none()
    if existing_evento is not None:
        abort(406, f"Já existe um evento cadastrado com o título '{titulo}'")

    capacidade = int(evento.get("capacidade_total", 0))
    if capacidade <= 0:
        abort(400, "A capacidade total deve ser um número inteiro maior que zero")

    preco_base = float(evento.get("preco_base", 0.0))
    if preco_base < 0:
        abort(400, "O preço base não pode ser negativo")

    novo_evento = Evento(
        titulo=titulo,
        descricao=evento.get("descricao", ""),
        categoria=evento.get("categoria", "Geral"),
        data_hora=evento.get("data_hora", ""),
        local=evento.get("local", ""),
        preco_base=preco_base,
        capacidade_total=capacidade,
        ingressos_disponiveis=capacidade,
        status="ATIVO",
    )

    db.session.add(novo_evento)
    db.session.commit()
    return evento_schema.dump(novo_evento), 201


def update(evento_id, evento):
    """
    Atualiza as informações cadastrais de um evento existente.
    """
    existing_evento = Evento.query.filter(Evento.id == evento_id).one_or_none()
    if not existing_evento:
        abort(404, f"Evento com ID {evento_id} não encontrado")

    novo_titulo = evento.get("titulo")
    if novo_titulo and novo_titulo != existing_evento.titulo:
        duplicado = Evento.query.filter(Evento.titulo == novo_titulo).one_or_none()
        if duplicado:
            abort(406, f"Outro evento já utiliza o título '{novo_titulo}'")
        existing_evento.titulo = novo_titulo

    if "descricao" in evento:
        existing_evento.descricao = evento["descricao"]
    if "categoria" in evento:
        existing_evento.categoria = evento["categoria"]
    if "data_hora" in evento:
        existing_evento.data_hora = evento["data_hora"]
    if "local" in evento:
        existing_evento.local = evento["local"]
    if "preco_base" in evento:
        existing_evento.preco_base = float(evento["preco_base"])

    db.session.merge(existing_evento)
    db.session.commit()
    return evento_schema.dump(existing_evento)


def delete(evento_id):
    """
    Exclui um evento e seus ingressos associados.
    """
    existing_evento = Evento.query.filter(Evento.id == evento_id).one_or_none()
    if existing_evento:
        db.session.delete(existing_evento)
        db.session.commit()
        return make_response(f"Evento com ID {evento_id} excluído com sucesso", 200)
    else:
        abort(404, f"Evento com ID {evento_id} não encontrado")
