#!/usr/bin/env python3
"""
Script para popular o banco com dados customizáveis
Uso: python -m app.utils.seed_custom --produtores 100 --propriedades 200 --associacoes 500
"""

import argparse
import random
from faker import Faker
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models import ProdutorRural, Propriedade, Safra, Cultura, PropriedadeSafraCultura
from app.utils.logger import app_logger
from app.utils.seed_data import seed_produtores, seed_safras, seed_culturas, seed_propriedades, \
    seed_propriedade_safra_cultura


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Função para popular o banco de dados com dados customizáveis
"""


def seed_custom_database(produtores_qty=50, propriedades_qty=100, associacoes_qty=200, safras_anos=None):
    """Popula o banco com quantidades customizáveis"""

    if safras_anos is None:
        safras_anos = list(range(2020, 2025))

    app_logger.info(f"Iniciando população customizada: {produtores_qty} produtores, "
                    f"{propriedades_qty} propriedades, {associacoes_qty} associações")

    db = next(get_db())

    try:
        # Verificar se já existem dados
        existing_produtores = db.query(ProdutorRural).count()
        if existing_produtores > 0:
            app_logger.warning("Banco já possui dados! Use --force para sobrescrever.")
            return

        # Criar dados em ordem
        produtores = seed_produtores(db, quantidade=produtores_qty)
        safras = seed_safras(db) if not safras_anos else seed_custom_safras(db, safras_anos)
        culturas = seed_culturas(db)
        propriedades = seed_propriedades(db, produtores, quantidade=propriedades_qty)
        associacoes = seed_propriedade_safra_cultura(db, propriedades, safras, culturas, quantidade=associacoes_qty)

        app_logger.info("Banco de dados populado com sucesso!")
        app_logger.info(f"Resumo: {len(produtores)} produtores, {len(propriedades)} propriedades, "
                        f"{len(safras)} safras, {len(culturas)} culturas, {len(associacoes)} associações")

    except Exception as e:
        app_logger.error(f"Erro ao popular banco: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


"""
Cria safras com anos customizados
"""


def seed_custom_safras(db: Session, anos):
    app_logger.info(f"Criando safras para os anos: {anos}")

    safras = []
    for ano in anos:
        safra = Safra(ano=ano)
        safras.append(safra)

    db.add_all(safras)
    db.commit()
    app_logger.info(f"{len(safras)} safras criadas com sucesso!")
    return safras


"""
Cria culturas customizadas
"""


def seed_custom_culturas(db: Session, culturas_list):
    app_logger.info(f"Criando culturas: {culturas_list}")

    culturas = []
    for nome in culturas_list:
        cultura = Cultura(nome=nome)
        culturas.append(cultura)

    db.add_all(culturas)
    db.commit()
    app_logger.info(f"{len(culturas)} culturas criadas com sucesso!")
    return culturas


"""
Cria associações entre propriedades, safras e culturas
"""


def main():
    parser = argparse.ArgumentParser(description='Popular banco com dados customizáveis')
    parser.add_argument('--produtores', type=int, default=50, help='Quantidade de produtores')
    parser.add_argument('--propriedades', type=int, default=100, help='Quantidade de propriedades')
    parser.add_argument('--associacoes', type=int, default=200, help='Quantidade de associações')
    parser.add_argument('--safras', nargs='+', type=int, help='Anos das safras (ex: 2020 2021 2022)')
    parser.add_argument('--culturas', nargs='+', help='Lista de culturas (ex: "Soja" "Milho" "Café")')
    parser.add_argument('--force', action='store_true', help='Forçar população (apaga dados existentes)')

    args = parser.parse_args()

    if args.force:
        # Limpar dados existentes
        db = next(get_db())
        try:
            app_logger.info("Limpando dados existentes...")
            db.query(PropriedadeSafraCultura).delete()
            db.query(Propriedade).delete()
            db.query(ProdutorRural).delete()
            db.query(Safra).delete()
            db.query(Cultura).delete()
            db.commit()
        except Exception as e:
            app_logger.error(f"Erro ao limpar dados: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    # Popular com dados customizados
    seed_custom_database(
        produtores_qty=args.produtores,
        propriedades_qty=args.propriedades,
        associacoes_qty=args.associacoes,
        safras_anos=args.safras
    )


if __name__ == "__main__":
    main()
