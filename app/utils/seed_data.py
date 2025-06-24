import random
from faker import Faker
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models import ProdutorRural, Propriedade, Safra, Cultura, PropriedadeSafraCultura
from app.utils.logger import app_logger


# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configurar Faker para português brasileiro
fake = Faker(['pt_BR'])

"""
Popula a tabela de produtores com dados mockados e CPF/CNPJ únicos
"""


def seed_produtores(db: Session, quantidade: int = 50):
    app_logger.info(f"Criando {quantidade} produtores...")

    produtores = []
    cpfs_cnpjs_gerados = set()
    while len(produtores) < quantidade:
        if random.choice([True, False]):
            doc = fake.cpf()
        else:
            doc = fake.cnpj()
        if doc in cpfs_cnpjs_gerados:
            continue  # pula duplicado
        cpfs_cnpjs_gerados.add(doc)
        produtor = ProdutorRural(
            nome=fake.name(),
            cpf_cnpj=doc
        )
        produtores.append(produtor)

    db.add_all(produtores)
    db.commit()
    app_logger.info(f"{quantidade} produtores criados com sucesso!")
    return produtores


"""
Popula a tabela de safras com anos recentes
"""


def seed_safras(db: Session):
    app_logger.info("Criando safras...")

    # Criar safras dos últimos 5 anos
    anos = list(range(2020, 2025))
    safras = []

    for ano in anos:
        safra = Safra(ano=ano)
        safras.append(safra)

    db.add_all(safras)
    db.commit()
    app_logger.info(f"{len(safras)} safras criadas com sucesso!")
    return safras


"""
Popula a tabela de culturas com culturas brasileiras
"""


def seed_culturas(db: Session):
    app_logger.info("Criando culturas...")

    culturas_nomes = [
        "Soja", "Milho", "Café", "Cana-de-açúcar", "Arroz",
        "Feijão", "Trigo", "Algodão", "Laranja", "Uva",
        "Banana", "Manga", "Abacaxi", "Melancia", "Tomate",
        "Cebola", "Batata", "Cenoura", "Alface", "Couve"
    ]

    culturas = []
    for nome in culturas_nomes:
        cultura = Cultura(nome=nome)
        culturas.append(cultura)

    db.add_all(culturas)
    db.commit()
    app_logger.info(f"{len(culturas)} culturas criadas com sucesso!")
    return culturas


"""
Popula a tabela de propriedades com dados mockados
"""


def seed_propriedades(db: Session, produtores, quantidade: int = 100):
    app_logger.info(f"Criando {quantidade} propriedades...")

    estados_brasil = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    propriedades = []
    for _ in range(quantidade):
        # Gerar áreas realistas
        area_total = round(random.uniform(50, 5000), 2)
        area_agricultavel = round(area_total * random.uniform(0.6, 0.9), 2)
        area_vegetacao = round(area_total - area_agricultavel, 2)

        propriedade = Propriedade(
            nome=f"Fazenda {fake.company()}",
            cidade=fake.city(),
            estado=random.choice(estados_brasil),
            area_total=area_total,
            area_agricultavel=area_agricultavel,
            area_vegetacao=area_vegetacao,
            produtor_id=random.choice(produtores).id
        )
        propriedades.append(propriedade)

    db.add_all(propriedades)
    db.commit()
    app_logger.info(f"{quantidade} propriedades criadas com sucesso!")
    return propriedades


"""
Popula a tabela de associações com dados mockados
"""


def seed_propriedade_safra_cultura(db: Session, propriedades, safras, culturas, quantidade: int = 200):
    app_logger.info(f"Criando {quantidade} associações...")

    associacoes = []
    for _ in range(quantidade):
        associacao = PropriedadeSafraCultura(
            propriedade_id=random.choice(propriedades).id,
            safra_id=random.choice(safras).id,
            cultura_id=random.choice(culturas).id
        )
        associacoes.append(associacao)

    db.add_all(associacoes)
    db.commit()
    app_logger.info(f"{quantidade} associações criadas com sucesso!")
    return associacoes


"""
Função principal para popular todo o banco de dados
"""


def seed_database():
    app_logger.info("Iniciando população do banco de dados...")

    # Obter sessão do banco
    db = next(get_db())

    try:
        # Verificar se já existem dados
        existing_produtores = db.query(ProdutorRural).count()
        if existing_produtores > 0:
            app_logger.warning("Banco já possui dados! Use --force para sobrescrever.")
            return

        # Criar dados em ordem
        produtores = seed_produtores(db, quantidade=50)
        safras = seed_safras(db)
        culturas = seed_culturas(db)
        propriedades = seed_propriedades(db, produtores, quantidade=100)
        associacoes = seed_propriedade_safra_cultura(db, propriedades, safras, culturas, quantidade=200)

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
Força a população do banco, apagando dados existentes
"""


def seed_database_force():
    app_logger.info("Forçando população do banco de dados...")

    db = next(get_db())

    try:
        # Limpar todas as tabelas
        app_logger.info("Limpando dados existentes...")
        db.query(PropriedadeSafraCultura).delete()
        db.query(Propriedade).delete()
        db.query(ProdutorRural).delete()
        db.query(Safra).delete()
        db.query(Cultura).delete()
        db.commit()

        # Recriar dados
        seed_database()

    except Exception as e:
        app_logger.error(f"Erro ao forçar população: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        seed_database_force()
    else:
        seed_database()
