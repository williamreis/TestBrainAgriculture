import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.database import Base
from app.models import ProdutorRural, Propriedade, Safra, Cultura, PropriedadeSafraCultura
# Importar todos os get_db das rotas
from app.routes.produtor import get_db as get_db_produtor
from app.routes.propriedade import get_db as get_db_propriedade
from app.routes.safra import get_db as get_db_safra
from app.routes.cultura import get_db as get_db_cultura
from app.routes.propriedade_safra_cultura import get_db as get_db_assoc
from app.routes.dashboard import get_db as get_db_dashboard

# Configuração do banco de teste em memória para isolamento
@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de teste isolada, usando a mesma conexão para todo o teste."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TransactionSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TransactionSession()
    yield session
    session.close()
    connection.close()


@pytest.fixture
def client(db_session):
    """Cria um cliente de teste com banco isolado e conexão fixa."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db_produtor] = override_get_db
    app.dependency_overrides[get_db_propriedade] = override_get_db
    app.dependency_overrides[get_db_safra] = override_get_db
    app.dependency_overrides[get_db_cultura] = override_get_db
    app.dependency_overrides[get_db_assoc] = override_get_db
    app.dependency_overrides[get_db_dashboard] = override_get_db
    return TestClient(app)


# Dados mockados para testes
@pytest.fixture
def mock_produtor_data():
    """Dados mockados para produtor com CPF válido"""
    return {
        "nome": "João Silva",
        "cpf_cnpj": "529.982.247-25"  # CPF válido
    }


@pytest.fixture
def mock_propriedade_data():
    """Dados mockados para propriedade"""
    return {
        "nome": "Fazenda São João",
        "cidade": "Goiânia",
        "estado": "GO",
        "area_total": 1000.0,
        "area_agricultavel": 800.0,
        "area_vegetacao": 200.0,
        "produtor_id": 1
    }


@pytest.fixture
def mock_safra_data():
    """Dados mockados para safra"""
    return {
        "ano": 2024
    }


@pytest.fixture
def mock_cultura_data():
    """Dados mockados para cultura"""
    return {
        "nome": "Soja"
    }


@pytest.fixture
def mock_propriedade_safra_cultura_data():
    """Dados mockados para associação"""
    return {
        "propriedade_id": 1,
        "safra_id": 1,
        "cultura_id": 1
    }


# Fixtures para criar dados no banco
@pytest.fixture
def sample_produtor(db_session):
    """Cria um produtor de exemplo no banco"""
    produtor = ProdutorRural(
        nome="Maria Santos",
        cpf_cnpj="98765432100"
    )
    db_session.add(produtor)
    db_session.commit()
    db_session.refresh(produtor)
    return produtor


@pytest.fixture
def sample_propriedade(db_session, sample_produtor):
    """Cria uma propriedade de exemplo no banco"""
    propriedade = Propriedade(
        nome="Fazenda Boa Vista",
        cidade="Brasília",
        estado="DF",
        area_total=500.0,
        area_agricultavel=400.0,
        area_vegetacao=100.0,
        produtor_id=sample_produtor.id
    )
    db_session.add(propriedade)
    db_session.commit()
    db_session.refresh(propriedade)
    return propriedade


@pytest.fixture
def sample_safra(db_session):
    """Cria uma safra de exemplo no banco"""
    safra = Safra(ano=2023)
    db_session.add(safra)
    db_session.commit()
    db_session.refresh(safra)
    return safra


@pytest.fixture
def sample_cultura(db_session):
    """Cria uma cultura de exemplo no banco"""
    cultura = Cultura(nome="Milho")
    db_session.add(cultura)
    db_session.commit()
    db_session.refresh(cultura)
    return cultura


@pytest.fixture
def sample_associacao(db_session, sample_propriedade, sample_safra, sample_cultura):
    """Cria uma associação de exemplo no banco"""
    associacao = PropriedadeSafraCultura(
        propriedade_id=sample_propriedade.id,
        safra_id=sample_safra.id,
        cultura_id=sample_cultura.id
    )
    db_session.add(associacao)
    db_session.commit()
    db_session.refresh(associacao)
    return associacao
