# Apresentação do Sistema de Nutrição

## Visão Geral

Este documento apresenta o Sistema de Nutrição desenvolvido para transformar a planilha de nutrição em um sistema integrado. O sistema foi construído com base nos requisitos identificados e validados, incluindo os módulos de cadastro de NFe, contratos e cotações, controle mensal, fechamento e análise, além do dashboard personalizado.

## Módulos Implementados

### 1. Módulo de Cadastro de NFe

Este módulo permite o registro completo de notas fiscais, essencial para a maioria das fórmulas e cálculos do sistema.

**Funcionalidades principais:**
- Cadastro de notas fiscais com todos os campos necessários
- Vinculação de itens da nota fiscal aos insumos
- Integração com fornecedores e contratos
- Relatórios de notas fiscais por período

### 2. Módulo de Contratos e Cotações

Mantém o formato atual utilizado na planilha, permitindo o gerenciamento de contratos e cotações.

**Funcionalidades principais:**
- Cadastro de contratos com cronograma de entregas
- Registro de cotações com histórico de preços
- Sistema de alertas para compras futuras
- Visualização de cronograma de entregas

### 3. Módulo de Controle Mensal

Substitui as abas mensais da planilha, centralizando os dados em um único local.

**Funcionalidades principais:**
- Registro de entregas por período
- Controle de estoque com entradas e saídas
- Acompanhamento de pagamentos
- Relatórios comparativos entre períodos

### 4. Módulo de Fechamento e Análise

Automatiza os cálculos de custo médio e gera relatórios de fechamento.

**Funcionalidades principais:**
- Cálculo automático de custo médio por insumo
- Geração de relatórios de fechamento mensal
- Análise de tendências de preços
- Exportação de dados para outros sistemas

### 5. Dashboard Integrado

Fornece uma visão geral e rápida das informações mais relevantes.

**Funcionalidades principais:**
- Visualização gráfica de dados importantes
- Indicadores de desempenho em tempo real
- Filtros interativos para análise personalizada
- Alertas visuais para situações críticas

## Como Executar o Sistema

### Backend

1. Navegue até a pasta raiz do projeto:
   ```
   cd /home/ubuntu/sistema_nutricao
   ```

2. Execute o script de inicialização do backend:
   ```
   bash run_backend.sh
   ```

3. O servidor backend estará disponível em http://localhost:5000

### Frontend

1. Navegue até a pasta frontend:
   ```
   cd /home/ubuntu/sistema_nutricao/frontend
   ```

2. Execute o script de inicialização do frontend:
   ```
   bash run_frontend.sh
   ```

3. A interface do usuário estará disponível em http://localhost:3000

## Próximos Passos

Após esta apresentação, gostaríamos de coletar seu feedback sobre:

1. Usabilidade da interface
2. Fluxos de trabalho implementados
3. Funcionalidades adicionais desejadas
4. Prioridades para as próximas iterações

Com base no seu feedback, planejamos as próximas etapas de desenvolvimento para garantir que o sistema atenda plenamente às suas necessidades.
