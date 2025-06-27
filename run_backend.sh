#!/bin/bash

# Script para iniciar o backend do Sistema de Nutrição

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Definir variáveis de ambiente
export FLASK_APP=backend
export FLASK_ENV=development
export DATABASE_URL="sqlite:///sistema_nutricao.db"
export SECRET_KEY="sistema-nutricao-secret-key"

# Criar banco de dados se não existir
echo "Inicializando banco de dados..."
flask db init || true
flask db migrate -m "Migração inicial" || true
flask db upgrade || true

# Iniciar o servidor
echo "Iniciando servidor backend..."
flask run --host=0.0.0.0 --port=5000
