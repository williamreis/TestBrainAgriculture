import pytest
from fastapi.testclient import TestClient
from app.models import ProdutorRural

"""
Testes para a API de Produtores
"""


class TestProdutoresAPI:

    def test_create_produtor_success(self, client, mock_produtor_data):
        """Testa criação bem-sucedida de produtor"""
        response = client.post("/produtores/", json=mock_produtor_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == mock_produtor_data["nome"]
        assert data["cpf_cnpj"] == mock_produtor_data["cpf_cnpj"]
        assert "id" in data

    """
    Testa criação com CPF inválido
    """

    def test_create_produtor_invalid_cpf(self, client):
        invalid_data = {
            "nome": "João Silva",
            "cpf_cnpj": "12345678900"  # CPF inválido
        }
        response = client.post("/produtores/", json=invalid_data)
        assert response.status_code == 400
        assert "CPF ou CNPJ inválido" in response.json()["detail"]

    """
    Testa criação com CPF duplicado
    """

    def test_create_produtor_duplicate_cpf(self, client, sample_produtor):
        duplicate_data = {
            "nome": "Outro Nome",
            "cpf_cnpj": sample_produtor.cpf_cnpj
        }
        response = client.post("/produtores/", json=duplicate_data)
        assert response.status_code == 400

    """
    Testa listagem de produtores
    """

    def test_list_produtores(self, client, sample_produtor):
        response = client.get("/produtores/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    """
    Testa busca de produtor por ID
    """

    def test_get_produtor_by_id(self, client, sample_produtor):
        response = client.get(f"/produtores/{sample_produtor.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_produtor.id
        assert data["nome"] == sample_produtor.nome

    """
    Testa busca de produtor inexistente
    """

    def test_get_produtor_not_found(self, client):
        response = client.get("/produtores/999")
        assert response.status_code == 404
        assert "Produtor não encontrado" in response.json()["detail"]

    """
    Testa atualização bem-sucedida de produtor
    """

    def test_update_produtor_success(self, client, sample_produtor):
        update_data = {"nome": "Nome Atualizado"}
        response = client.put(f"/produtores/{sample_produtor.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Nome Atualizado"
        assert data["cpf_cnpj"] == sample_produtor.cpf_cnpj

    """
    Testa atualização com CPF inválido
    """

    def test_update_produtor_invalid_cpf(self, client, sample_produtor):
        update_data = {"cpf_cnpj": "12345678900"}
        response = client.put(f"/produtores/{sample_produtor.id}", json=update_data)
        assert response.status_code == 400
        assert "CPF ou CNPJ inválido" in response.json()["detail"]

    """
    Testa atualização de produtor inexistente
    """

    def test_update_produtor_not_found(self, client):
        update_data = {"nome": "Nome Atualizado"}
        response = client.put("/produtores/999", json=update_data)
        assert response.status_code == 404
        assert "Produtor não encontrado" in response.json()["detail"]

    """
    Testa exclusão bem-sucedida de produtor
    """

    def test_delete_produtor_success(self, client, sample_produtor):
        response = client.delete(f"/produtores/{sample_produtor.id}")
        assert response.status_code == 204

    """
    Testa exclusão de produtor inexistente
    """

    def test_delete_produtor_not_found(self, client):
        response = client.delete("/produtores/999")
        assert response.status_code == 404
        assert "Produtor não encontrado" in response.json()["detail"]


"""
Testes para validações de negócio
"""


class TestProdutorValidations:
    """
    Testa CPF válido
    """

    def test_valid_cpf(self, client):
        valid_data = {
            "nome": "João Silva",
            "cpf_cnpj": "529.982.247-25"  # CPF válido
        }
        response = client.post("/produtores/", json=valid_data)
        assert response.status_code == 201

    """
    Testa CNPJ válido
    """

    def test_valid_cnpj(self, client):
        valid_data = {
            "nome": "Empresa Devs LTDA",
            "cpf_cnpj": "11.222.333/0001-81"  # CNPJ válido
        }
        response = client.post("/produtores/", json=valid_data)
        assert response.status_code == 201

    """
    Testa CPF/CNPJ inválido
    """

    def test_invalid_cpf_cnpj(self, client):
        invalid_data = {
            "nome": "João da Silva",
            "cpf_cnpj": "123.456.789-00"  # Inválido
        }
        response = client.post("/produtores/", json=invalid_data)
        assert response.status_code == 400
