# Documentação do Sistema de Nutrição

## Visão Geral

O Sistema de Nutrição é uma aplicação completa para gerenciamento de contratos, cotações, controle mensal e análise de custos relacionados à nutrição. O sistema foi desenvolvido para substituir a planilha Excel anteriormente utilizada, oferecendo maior robustez, segurança e funcionalidades avançadas.

## Arquitetura

O sistema foi desenvolvido utilizando uma arquitetura moderna de três camadas:

1. **Frontend**: Interface de usuário desenvolvida com React e Material-UI
2. **Backend**: API RESTful desenvolvida com Flask e SQLAlchemy
3. **Banco de Dados**: Sistema de persistência utilizando SQLite (desenvolvimento) ou PostgreSQL (produção)

## Módulos Principais

### 1. Módulo de Cadastro de NFe

Este módulo gerencia o cadastro e controle de notas fiscais, fornecedores e insumos.

**Principais funcionalidades:**
- Cadastro e gestão de fornecedores
- Cadastro e gestão de insumos
- Registro de notas fiscais com múltiplos itens
- Consulta e relatórios de notas fiscais

### 2. Módulo de Contratos e Cotações

Este módulo gerencia contratos com fornecedores, cotações de preços e planejamento de compras.

**Principais funcionalidades:**
- Cadastro e gestão de contratos
- Registro de cotações de preços
- Planejamento de compras futuras
- Cronograma de entregas
- Análise de evolução de preços

### 3. Módulo de Controle Mensal

Este módulo substitui as abas mensais da planilha, permitindo o controle de entregas e estoque.

**Principais funcionalidades:**
- Registro mensal por insumo
- Controle de entregas
- Acompanhamento de estoque
- Programação de entregas futuras
- Evolução de estoque

### 4. Módulo de Fechamento e Análise

Este módulo realiza cálculos de custo médio e gera relatórios analíticos.

**Principais funcionalidades:**
- Cálculo de custo médio por insumo
- Fechamento mensal
- Relatórios de tendência de preços
- Análises comparativas
- Dashboards analíticos

### 5. Módulo de Autenticação

Este módulo gerencia o acesso ao sistema e o controle de permissões.

**Principais funcionalidades:**
- Autenticação de usuários
- Controle de níveis de acesso
- Registro de atividades (logs)
- Gerenciamento de perfis

## Endpoints da API

### Autenticação
- `POST /api/auth/login`: Autenticação de usuário
- `POST /api/auth/logout`: Encerramento de sessão
- `GET /api/auth/perfil`: Consulta do perfil do usuário logado
- `PUT /api/auth/perfil`: Atualização do perfil do usuário logado

### Fornecedores
- `GET /api/fornecedores`: Lista de fornecedores
- `POST /api/fornecedores`: Cadastro de fornecedor
- `GET /api/fornecedores/{id}`: Detalhes de um fornecedor
- `PUT /api/fornecedores/{id}`: Atualização de fornecedor
- `DELETE /api/fornecedores/{id}`: Exclusão de fornecedor

### Insumos
- `GET /api/insumos`: Lista de insumos
- `POST /api/insumos`: Cadastro de insumo
- `GET /api/insumos/{id}`: Detalhes de um insumo
- `PUT /api/insumos/{id}`: Atualização de insumo
- `DELETE /api/insumos/{id}`: Exclusão de insumo

### Notas Fiscais
- `GET /api/nfe`: Lista de notas fiscais
- `POST /api/nfe`: Cadastro de nota fiscal
- `GET /api/nfe/{id}`: Detalhes de uma nota fiscal
- `PUT /api/nfe/{id}`: Atualização de nota fiscal
- `DELETE /api/nfe/{id}`: Exclusão de nota fiscal

### Contratos
- `GET /api/contratos`: Lista de contratos
- `POST /api/contratos`: Cadastro de contrato
- `GET /api/contratos/{id}`: Detalhes de um contrato
- `PUT /api/contratos/{id}`: Atualização de contrato
- `DELETE /api/contratos/{id}`: Exclusão de contrato
- `GET /api/contratos/cronograma`: Cronograma de contratos

### Cotações
- `GET /api/cotacoes`: Lista de cotações
- `POST /api/cotacoes`: Cadastro de cotação
- `GET /api/cotacoes/{id}`: Detalhes de uma cotação
- `PUT /api/cotacoes/{id}`: Atualização de cotação
- `DELETE /api/cotacoes/{id}`: Exclusão de cotação
- `GET /api/cotacoes/evolucao-precos`: Evolução de preços

### Controle Mensal
- `GET /api/controle-mensal/registros`: Lista de registros mensais
- `POST /api/controle-mensal/registros`: Cadastro de registro mensal
- `GET /api/controle-mensal/registros/{id}`: Detalhes de um registro mensal
- `PUT /api/controle-mensal/registros/{id}`: Atualização de registro mensal
- `DELETE /api/controle-mensal/registros/{id}`: Exclusão de registro mensal
- `GET /api/controle-mensal/evolucao-estoque`: Evolução de estoque

### Fechamento
- `GET /api/fechamento`: Lista de fechamentos mensais
- `POST /api/fechamento`: Cadastro de fechamento mensal
- `GET /api/fechamento/{id}`: Detalhes de um fechamento mensal
- `POST /api/fechamento/{id}/fechar`: Fechamento de um período
- `POST /api/fechamento/{id}/reabrir`: Reabertura de um período
- `GET /api/fechamento/relatorio/custo-medio`: Relatório de custo médio
- `GET /api/fechamento/relatorio/tendencia-precos`: Relatório de tendência de preços

## Instruções de Execução

### Requisitos
- Python 3.8+
- Node.js 14+
- PostgreSQL (produção)

### Instalação e Execução

1. Clone o repositório
2. Configure o ambiente virtual Python:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. Execute o backend:
   ```
   ./run_backend.sh
   ```
4. Execute o frontend:
   ```
   cd frontend
   npm install
   npm start
   ```

### Testes

Para executar os testes de integração:
```
./run_tests.sh
```

## Próximos Passos

1. Implementação de relatórios avançados
2. Integração com sistemas externos
3. Aplicativo móvel para consultas rápidas
4. Melhorias de performance e escalabilidade
