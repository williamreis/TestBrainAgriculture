# Especificação OpenAPI - TestBrainAgriculture

## Visão Geral

A API do TestBrainAgriculture fornece endpoints para gerenciamento completo de produtores rurais, propriedades, safras e culturas, seguindo as especificações OpenAPI 3.0.

## Base URL
```
http://localhost:8008
```

## Autenticação
Atualmente a API não requer autenticação. Todos os endpoints são públicos.

## Endpoints

### 1. Produtores Rurais

#### GET /produtores/
**Descrição**: Lista todos os produtores rurais cadastrados

**Resposta**:
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "cpf_cnpj": "123.456.789-01"
  }
]
```

#### POST /produtores/
**Descrição**: Cria um novo produtor rural

**Request Body**:
```json
{
  "nome": "João Silva",
  "cpf_cnpj": "123.456.789-01"
}
```

**Validações**:
- `nome`: String obrigatória, mínimo 2 caracteres
- `cpf_cnpj`: CPF ou CNPJ válido, único no sistema

**Resposta**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf_cnpj": "123.456.789-01"
}
```

#### GET /produtores/{id}
**Descrição**: Busca um produtor específico por ID

**Parâmetros**:
- `id`: ID do produtor (integer)

**Resposta**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf_cnpj": "123.456.789-01"
}
```

#### PUT /produtores/{id}
**Descrição**: Atualiza um produtor existente

**Parâmetros**:
- `id`: ID do produtor (integer)

**Request Body**:
```json
{
  "nome": "João Silva Atualizado",
  "cpf_cnpj": "123.456.789-01"
}
```

#### DELETE /produtores/{id}
**Descrição**: Remove um produtor do sistema

**Parâmetros**:
- `id`: ID do produtor (integer)

### 2. Propriedades

#### GET /propriedades/
**Descrição**: Lista todas as propriedades cadastradas

**Resposta**:
```json
[
  {
    "id": 1,
    "nome": "Fazenda São João",
    "cidade": "Goiânia",
    "estado": "GO",
    "area_total": 1000.0,
    "area_agricultavel": 800.0,
    "area_vegetacao": 200.0,
    "produtor_id": 1
  }
]
```

#### POST /propriedades/
**Descrição**: Cria uma nova propriedade

**Request Body**:
```json
{
  "nome": "Fazenda São João",
  "cidade": "Goiânia",
  "estado": "GO",
  "area_total": 1000.0,
  "area_agricultavel": 800.0,
  "area_vegetacao": 200.0,
  "produtor_id": 1
}
```

**Validações**:
- `nome`: String obrigatória
- `cidade`: String obrigatória
- `estado`: Sigla de estado válida (2 caracteres)
- `area_total`: Float positivo
- `area_agricultavel`: Float positivo, <= area_total
- `area_vegetacao`: Float positivo, <= area_total
- `area_total` = `area_agricultavel` + `area_vegetacao`
- `produtor_id`: ID de produtor existente

### 3. Safras

#### GET /safras/
**Descrição**: Lista todas as safras cadastradas

**Resposta**:
```json
[
  {
    "id": 1,
    "ano": 2024
  }
]
```

#### POST /safras/
**Descrição**: Cria uma nova safra

**Request Body**:
```json
{
  "ano": 2024
}
```

**Validações**:
- `ano`: Integer entre 1900 e 2100

### 4. Culturas

#### GET /culturas/
**Descrição**: Lista todas as culturas cadastradas

**Resposta**:
```json
[
  {
    "id": 1,
    "nome": "Soja"
  }
]
```

#### POST /culturas/
**Descrição**: Cria uma nova cultura

**Request Body**:
```json
{
  "nome": "Soja"
}
```

**Validações**:
- `nome`: String obrigatória, único no sistema

### 5. Associações Propriedade-Safra-Cultura

#### GET /propriedade-safra-cultura/
**Descrição**: Lista todas as associações

**Resposta**:
```json
[
  {
    "id": 1,
    "propriedade_id": 1,
    "safra_id": 1,
    "cultura_id": 1
  }
]
```

#### POST /propriedade-safra-cultura/
**Descrição**: Cria uma nova associação

**Request Body**:
```json
{
  "propriedade_id": 1,
  "safra_id": 1,
  "cultura_id": 1
}
```

**Validações**:
- `propriedade_id`: ID de propriedade existente
- `safra_id`: ID de safra existente
- `cultura_id`: ID de cultura existente
- Combinação única de propriedade + safra + cultura

### 6. Dashboard

#### GET /dashboard/
**Descrição**: Retorna dados consolidados para o dashboard

**Resposta**:
```json
{
  "estatisticas": {
    "total_fazendas": 100,
    "total_hectares": 50000.0
  },
  "grafico_estados": [
    {
      "estado": "GO",
      "quantidade": 25,
      "percentual": 25.0
    }
  ],
  "grafico_culturas": [
    {
      "cultura": "Soja",
      "quantidade": 50,
      "percentual": 50.0
    }
  ],
  "grafico_uso_solo": [
    {
      "tipo": "Área Agricultável",
      "area": 40000.0,
      "percentual": 80.0
    }
  ]
}
```

#### GET /dashboard/estatisticas
**Descrição**: Retorna apenas as estatísticas gerais

#### GET /dashboard/grafico-estados
**Descrição**: Retorna dados para gráfico por estados

#### GET /dashboard/grafico-culturas
**Descrição**: Retorna dados para gráfico por culturas

#### GET /dashboard/grafico-uso-solo
**Descrição**: Retorna dados para gráfico de uso do solo

## Códigos de Status HTTP

- **200**: Sucesso
- **201**: Criado com sucesso
- **204**: Sucesso sem conteúdo (DELETE)
- **400**: Erro de validação
- **404**: Recurso não encontrado
- **422**: Erro de validação de dados
- **500**: Erro interno do servidor

## Exemplos de Erro

### Erro de Validação (400)
```json
{
  "detail": "CPF ou CNPJ inválido"
}
```

### Recurso não encontrado (404)
```json
{
  "detail": "Produtor não encontrado"
}
```

### Erro de validação de dados (422)
```json
{
  "detail": [
    {
      "loc": ["body", "nome"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Schemas de Validação

### ProdutorRural
```json
{
  "type": "object",
  "properties": {
    "nome": {
      "type": "string",
      "minLength": 2
    },
    "cpf_cnpj": {
      "type": "string",
      "pattern": "^(\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}|\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2})$"
    }
  },
  "required": ["nome", "cpf_cnpj"]
}
```

### Propriedade
```json
{
  "type": "object",
  "properties": {
    "nome": {
      "type": "string"
    },
    "cidade": {
      "type": "string"
    },
    "estado": {
      "type": "string",
      "pattern": "^[A-Z]{2}$"
    },
    "area_total": {
      "type": "number",
      "minimum": 0
    },
    "area_agricultavel": {
      "type": "number",
      "minimum": 0
    },
    "area_vegetacao": {
      "type": "number",
      "minimum": 0
    },
    "produtor_id": {
      "type": "integer"
    }
  },
  "required": ["nome", "cidade", "estado", "area_total", "area_agricultavel", "area_vegetacao", "produtor_id"]
}
```

## Rate Limiting

Atualmente não há limite de requisições por minuto.

## Versionamento

A API está na versão 1.0. Mudanças futuras serão versionadas adequadamente.

## Documentação Interativa

Acesse a documentação interativa da API em:
```
http://localhost:8008/docs
```

## Testes da API

### Exemplo com curl

```bash
# Listar produtores
curl -X GET "http://localhost:8008/produtores/"

# Criar produtor
curl -X POST "http://localhost:8008/produtores/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "cpf_cnpj": "123.456.789-01"}'

# Buscar produtor por ID
curl -X GET "http://localhost:8008/produtores/1"

# Dashboard
curl -X GET "http://localhost:8008/dashboard/"
```

### Exemplo com Python

```python
import requests

# Listar produtores
response = requests.get("http://localhost:8008/produtores/")
produtores = response.json()

# Criar produtor
data = {"nome": "João Silva", "cpf_cnpj": "123.456.789-01"}
response = requests.post("http://localhost:8008/produtores/", json=data)
novo_produtor = response.json()

# Dashboard
response = requests.get("http://localhost:8008/dashboard/")
dashboard_data = response.json()
``` 