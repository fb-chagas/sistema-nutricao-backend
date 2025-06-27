# Plano de Desenvolvimento do Sistema de Nutrição

## Visão Geral
Este documento descreve a estrutura do backend e banco de dados para o sistema completo de nutrição, baseado na versão demonstrativa aprovada pelo cliente. O sistema será desenvolvido com foco em qualidade, robustez e integração entre todos os módulos.

## Arquitetura do Sistema

### Stack Tecnológica
- **Backend**: Flask (Python)
- **Frontend**: React com TypeScript
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Hospedagem**: A definir com o cliente

### Estrutura de Diretórios
```
sistema_nutricao/
├── backend/
│   ├── api/
│   │   ├── nfe_routes.py
│   │   ├── contratos_routes.py
│   │   ├── controle_mensal_routes.py
│   │   ├── fechamento_routes.py
│   │   └── auth_routes.py
│   ├── models/
│   │   ├── nfe_models.py
│   │   ├── contratos_models.py
│   │   ├── controle_mensal_models.py
│   │   ├── fechamento_models.py
│   │   └── user_models.py
│   ├── services/
│   │   ├── nfe_service.py
│   │   ├── contratos_service.py
│   │   ├── controle_mensal_service.py
│   │   ├── fechamento_service.py
│   │   └── auth_service.py
│   ├── utils/
│   │   ├── validators.py
│   │   ├── calculators.py
│   │   └── exporters.py
│   ├── config.py
│   ├── __init__.py
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
├── migrations/
├── tests/
├── docker-compose.yml
└── README.md
```

## Modelo de Dados

### Módulo de Cadastro de NFe
- **Fornecedores**: Informações de fornecedores
- **Insumos**: Cadastro de insumos utilizados
- **NotasFiscais**: Registro de notas fiscais
- **ItensNotaFiscal**: Itens de cada nota fiscal

### Módulo de Contratos e Cotações
- **Contratos**: Contratos com fornecedores
- **ItensContrato**: Itens de cada contrato
- **Cotacoes**: Cotações de preços
- **PlanejamentoCompra**: Planejamento de compras futuras

### Módulo de Controle Mensal
- **RegistrosMensais**: Controle mensal por insumo
- **EntregasMensais**: Registro de entregas
- **ProgramacoesFuturas**: Programação de entregas futuras

### Módulo de Fechamento e Análise
- **CustosMedios**: Cálculo de custo médio por insumo
- **FechamentosMensais**: Fechamento mensal
- **DetalhesFechamento**: Detalhes de cada fechamento
- **AnalisesComparativas**: Análises e comparativos

### Módulo de Autenticação
- **Usuarios**: Usuários do sistema
- **Perfis**: Perfis de acesso
- **Permissoes**: Permissões por perfil

## Diagrama de Entidade-Relacionamento (Simplificado)

```
Fornecedor 1--* NotaFiscal
Insumo 1--* ItemNotaFiscal
NotaFiscal 1--* ItemNotaFiscal

Fornecedor 1--* Contrato
Insumo 1--* ItemContrato
Contrato 1--* ItemContrato
Fornecedor 1--* Cotacao
Insumo 1--* Cotacao
Insumo 1--* PlanejamentoCompra

Insumo 1--* RegistroMensal
RegistroMensal 1--* EntregaMensal
NotaFiscal 0--* EntregaMensal
Contrato 0--* EntregaMensal
Insumo 1--* ProgramacaoFutura
Contrato 0--* ProgramacaoFutura

Insumo 1--* CustoMedio
FechamentoMensal 1--* DetalhesFechamento
Insumo 1--* DetalhesFechamento

Usuario *--1 Perfil
Perfil *--* Permissao
```

## APIs e Endpoints

### Módulo de Cadastro de NFe
- `GET /api/fornecedores`: Lista de fornecedores
- `POST /api/fornecedores`: Criar fornecedor
- `GET /api/insumos`: Lista de insumos
- `POST /api/insumos`: Criar insumo
- `GET /api/nfe`: Lista de notas fiscais
- `POST /api/nfe`: Criar nota fiscal
- `GET /api/nfe/{id}`: Detalhes de nota fiscal
- `PUT /api/nfe/{id}`: Atualizar nota fiscal
- `DELETE /api/nfe/{id}`: Excluir nota fiscal

### Módulo de Contratos e Cotações
- `GET /api/contratos`: Lista de contratos
- `POST /api/contratos`: Criar contrato
- `GET /api/contratos/{id}`: Detalhes de contrato
- `PUT /api/contratos/{id}`: Atualizar contrato
- `DELETE /api/contratos/{id}`: Excluir contrato
- `GET /api/cotacoes`: Lista de cotações
- `POST /api/cotacoes`: Criar cotação
- `GET /api/planejamento`: Lista de planejamentos
- `POST /api/planejamento`: Criar planejamento

### Módulo de Controle Mensal
- `GET /api/controle-mensal/registros`: Lista de registros mensais
- `POST /api/controle-mensal/registros`: Criar registro mensal
- `GET /api/controle-mensal/registros/{id}`: Detalhes de registro
- `PUT /api/controle-mensal/registros/{id}`: Atualizar registro
- `GET /api/controle-mensal/registros/{id}/entregas`: Entregas de um registro
- `POST /api/controle-mensal/registros/{id}/entregas`: Adicionar entrega
- `GET /api/programacao`: Lista de programações futuras
- `POST /api/programacao`: Criar programação futura

### Módulo de Fechamento e Análise
- `GET /api/fechamento/custo-medio`: Lista de custos médios
- `POST /api/fechamento/custo-medio/calcular`: Calcular custo médio
- `GET /api/fechamento`: Lista de fechamentos
- `POST /api/fechamento`: Criar fechamento
- `GET /api/fechamento/{id}`: Detalhes de fechamento
- `POST /api/fechamento/{id}/fechar`: Fechar fechamento
- `POST /api/fechamento/{id}/reabrir`: Reabrir fechamento
- `GET /api/analise`: Lista de análises
- `POST /api/analise`: Criar análise
- `GET /api/fechamento/relatorio/custo-medio`: Relatório de custo médio
- `GET /api/fechamento/relatorio/tendencia-precos`: Relatório de tendência

### Módulo de Autenticação
- `POST /api/auth/login`: Login
- `POST /api/auth/logout`: Logout
- `GET /api/auth/me`: Informações do usuário atual
- `GET /api/usuarios`: Lista de usuários
- `POST /api/usuarios`: Criar usuário
- `GET /api/perfis`: Lista de perfis
- `POST /api/perfis`: Criar perfil

## Próximos Passos
1. Configuração do ambiente de desenvolvimento
2. Implementação do banco de dados e modelos
3. Desenvolvimento das APIs do backend
4. Integração com o frontend
5. Testes unitários e de integração
6. Documentação do sistema
7. Implantação da primeira versão funcional
