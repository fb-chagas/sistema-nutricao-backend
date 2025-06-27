#!/bin/bash

# Script para executar o sistema de nutrição em modo de desenvolvimento

# Configurar ambiente
echo "Configurando ambiente de desenvolvimento..."

# Verificar se o diretório de testes existe
if [ ! -d "tests" ]; then
    mkdir -p tests
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r backend/requirements.txt
pip install pytest pytest-flask

# Executar testes de integração
echo "Executando testes de integração..."
python -m pytest tests/test_integracao.py -v

# Iniciar o backend
echo "Iniciando o backend..."
cd backend
export FLASK_APP=__init__.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000 &
BACKEND_PID=$!

echo "Backend iniciado com PID: $BACKEND_PID"
echo "Acesse o sistema em: http://localhost:5000"
echo "Para parar o sistema, pressione Ctrl+C"

# Função para limpar ao encerrar
cleanup() {
    echo "Encerrando o sistema..."
    kill $BACKEND_PID
    exit 0
}

# Capturar sinal de interrupção
trap cleanup SIGINT

# Manter o script rodando
wait $BACKEND_PID
