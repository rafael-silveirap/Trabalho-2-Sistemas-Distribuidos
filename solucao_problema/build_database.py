"""
Script para inicializar e popular o banco de dados SQLite (eventos.db)
com eventos e ingressos de demonstração para a EventPass API.
"""
import sys
import pathlib
import uuid

basedir = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(basedir))

import config
from models import Evento, Ingresso, db

EVENTOS_INICIAIS = [
    {
        "titulo": "Festival Indie Rock Brasil 2026",
        "descricao": "O maior festival independente do país com mais de 15 atrações nacionais e internacionais, praça de alimentação e ativações artísticas.",
        "categoria": "Show",
        "data_hora": "2026-11-14 18:00",
        "local": "Parque Ibirapuera - Arena Open Air",
        "preco_base": 180.00,
        "capacidade_total": 500,
        "ingressos_disponiveis": 497,
        "status": "ATIVO",
    },
    {
        "titulo": "Simpósio de Sistemas Distribuídos & Cloud",
        "descricao": "Conferência técnica abordando consenso distribuído, microsserviços tolerantes a falhas, escalabilidade horizontal e arquiteturas de alta disponibilidade.",
        "categoria": "Congresso",
        "data_hora": "2026-11-25 09:00",
        "local": "Centro de Convenções Rebouças - Auditório A",
        "preco_base": 240.00,
        "capacidade_total": 200,
        "ingressos_disponiveis": 198,
        "status": "ATIVO",
    },
    {
        "titulo": "Espetáculo Teatral: O Fantasma da Ópera",
        "descricao": "Superprodução musical aclamada pela crítica, com orquestra ao vivo e elenco estelar nos principais papéis.",
        "categoria": "Teatro",
        "data_hora": "2026-12-05 20:30",
        "local": "Teatro Municipal - Sala Nobre",
        "preco_base": 120.00,
        "capacidade_total": 150,
        "ingressos_disponiveis": 149,
        "status": "ATIVO",
    },
    {
        "titulo": "Workshop de Inteligência Artificial Aplicada",
        "descricao": "Treinamento prático 'hands-on' para desenvolvedores construírem agentes autônomos e pipelines de Machine Learning modernos.",
        "categoria": "Workshop",
        "data_hora": "2026-12-12 14:00",
        "local": "Hub de Inovação Tecnológica - Sala Tech",
        "preco_base": 90.00,
        "capacidade_total": 30,
        "ingressos_disponiveis": 0,
        "status": "ESGOTADO",  # Exemplo de evento já esgotado para validar regras de negócio
    },
]


def build_database():
    with config.app.app_context():
        db_path = config.basedir / "eventos.db"
        if db_path.exists():
            db_path.unlink()
            print(f"Banco existente '{db_path.name}' removido para reinicialização limpa.")

        db.create_all()
        print("Tabelas 'evento' e 'ingresso' criadas com sucesso.")

        eventos_inseridos = []
        for ev in EVENTOS_INICIAIS:
            evento = Evento(**ev)
            db.session.add(evento)
            eventos_inseridos.append(evento)

        db.session.commit()

        # Inserção de alguns bilhetes de teste vinculados
        ingressos_iniciais = [
            Ingresso(
                codigo_bilhete="TKT-DEMO0001",
                evento_id=eventos_inseridos[0].id,
                comprador_nome="Mariana Costa",
                comprador_email="mariana@email.com",
                tipo="MEIA",
                valor_pago=90.00,
                status="CONFIRMADO",
            ),
            Ingresso(
                codigo_bilhete="TKT-DEMO0002",
                evento_id=eventos_inseridos[0].id,
                comprador_nome="Carlos Eduardo",
                comprador_email="carlos@email.com",
                tipo="INTEIRA",
                valor_pago=180.00,
                status="CONFIRMADO",
            ),
            Ingresso(
                codigo_bilhete="TKT-DEMO0003",
                evento_id=eventos_inseridos[0].id,
                comprador_nome="Beatriz Lima",
                comprador_email="beatriz@email.com",
                tipo="VIP",
                valor_pago=270.00,
                status="CONFIRMADO",
            ),
            Ingresso(
                codigo_bilhete="TKT-DEMO0004",
                evento_id=eventos_inseridos[1].id,
                comprador_nome="Rodrigo Alves",
                comprador_email="rodrigo@email.com",
                tipo="INTEIRA",
                valor_pago=240.00,
                status="CONFIRMADO",
            ),
            Ingresso(
                codigo_bilhete="TKT-DEMO0005",
                evento_id=eventos_inseridos[1].id,
                comprador_nome="Fernanda Souza",
                comprador_email="fernanda@email.com",
                tipo="MEIA",
                valor_pago=120.00,
                status="CONFIRMADO",
            ),
            Ingresso(
                codigo_bilhete="TKT-DEMO0006",
                evento_id=eventos_inseridos[2].id,
                comprador_nome="Gustavo Mendes",
                comprador_email="gustavo@email.com",
                tipo="INTEIRA",
                valor_pago=120.00,
                status="CONFIRMADO",
            ),
        ]

        for ing in ingressos_iniciais:
            db.session.add(ing)

        db.session.commit()
        print(f"Banco populado com {len(eventos_inseridos)} eventos e {len(ingressos_iniciais)} bilhetes de exemplo!")


if __name__ == "__main__":
    build_database()
