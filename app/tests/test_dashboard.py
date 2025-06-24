import pytest
from fastapi.testclient import TestClient

"""
Testes para a API do Dashboard
"""


class TestDashboardAPI:
    """
    Testa endpoint principal do dashboard
    """

    def test_dashboard_data(self, client, sample_produtor, sample_propriedade, sample_associacao):
        response = client.get("/dashboard/")
        assert response.status_code == 200
        data = response.json()

        # Verificar estrutura da resposta
        assert "estatisticas" in data
        assert "grafico_estados" in data
        assert "grafico_culturas" in data
        assert "grafico_uso_solo" in data

        # Verificar estatísticas
        stats = data["estatisticas"]
        assert "total_fazendas" in stats
        assert "total_hectares" in stats
        assert isinstance(stats["total_fazendas"], int)
        assert isinstance(stats["total_hectares"], float)

    """
    Testa endpoint de estatísticas
    """

    def test_dashboard_estatisticas(self, client, sample_propriedade):
        response = client.get("/dashboard/estatisticas")
        assert response.status_code == 200
        data = response.json()

        assert "total_fazendas" in data
        assert "total_hectares" in data
        assert data["total_fazendas"] >= 1
        assert data["total_hectares"] > 0

    """
    Testa endpoint de gráfico por estados
    """

    def test_dashboard_grafico_estados(self, client, sample_propriedade):
        response = client.get("/dashboard/grafico-estados")
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        if data:  # Se há dados
            item = data[0]
            assert "estado" in item
            assert "quantidade" in item
            assert "percentual" in item

    """
    Testa endpoint de gráfico por culturas
    """

    def test_dashboard_grafico_culturas(self, client, sample_associacao):
        response = client.get("/dashboard/grafico-culturas")
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        if data:  # Se há dados
            item = data[0]
            assert "cultura" in item
            assert "quantidade" in item
            assert "percentual" in item

    """
    Testa endpoint de gráfico de uso do solo
    """

    def test_dashboard_grafico_uso_solo(self, client, sample_propriedade):
        response = client.get("/dashboard/grafico-uso-solo")
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        if data:  # Se há dados
            item = data[0]
            assert "tipo" in item
            assert "area" in item
            assert "percentual" in item

    """
    Testar dashboard com dados vazios
    """

    def test_dashboard_empty_data(self, client):
        # Usar um cliente limpo sem dados
        response = client.get("/dashboard/")
        assert response.status_code == 200
        data = response.json()

        # Deve retornar estrutura válida mesmo sem dados
        assert data["estatisticas"]["total_fazendas"] == 0
        assert data["estatisticas"]["total_hectares"] == 0.0
        assert isinstance(data["grafico_estados"], list)
        assert isinstance(data["grafico_culturas"], list)
        assert isinstance(data["grafico_uso_solo"], list)


"""
Testes para cálculos do dashboard
"""


class TestDashboardCalculations:
    """
    Testa cálculos de área
    """

    def test_area_calculations(self, client, sample_propriedade):
        response = client.get("/dashboard/grafico-uso-solo")
        assert response.status_code == 200
        data = response.json()

        if data:
            # Verificar se as áreas somam o total
            areas = {item["tipo"]: item["area"] for item in data}
            total_area = sample_propriedade.area_total

            if "Área Agricultável" in areas and "Área de Vegetação" in areas:
                calculated_total = areas["Área Agricultável"] + areas["Área de Vegetação"]
                # Ajustar para considerar apenas a propriedade de teste
                assert abs(calculated_total - total_area) < 0.01  # Tolerância para float

    """
    Testa cálculos de percentual
    """

    def test_percentual_calculations(self, client, sample_propriedade):
        response = client.get("/dashboard/grafico-uso-solo")
        assert response.status_code == 200
        data = response.json()

        if data:
            # Verificar se os percentuais somam aproximadamente 100%
            percentuais = [item["percentual"] for item in data]
            total_percentual = sum(percentuais)
            assert abs(total_percentual - 100.0) < 0.01  # Tolerância para float
