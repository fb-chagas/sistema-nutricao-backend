#!/bin/bash

# Script para executar os testes de integração do Sistema de Nutrição

echo "Iniciando testes de integração do Sistema de Nutrição..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências necessárias para testes
echo "Instalando dependências para testes..."
pip install pytest pytest-flask pytest-cov

# Executar testes com cobertura
echo "Executando testes de integração com análise de cobertura..."
python -m pytest tests/test_integracao.py -v --cov=backend --cov-report=term --cov-report=html:coverage_report

# Verificar resultado dos testes
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram com sucesso!"
    echo "Relatório de cobertura gerado em: coverage_report/index.html"
else
    echo "❌ Alguns testes falharam. Verifique os erros acima."
fi

# Desativar ambiente virtual
deactivate

echo "Testes de integração concluídos."
