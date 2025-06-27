@echo off
echo Iniciando Sistema de Nutrição...

:: Ativar ambiente virtual se não estiver ativado
if not defined VIRTUAL_ENV (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate
)

:: Instalar dependências
echo Instalando dependências...
pip install flask flask-sqlalchemy flask-login flask-cors marshmallow

:: Definir variáveis de ambiente
set FLASK_APP=backend
set FLASK_ENV=development
set DATABASE_URL=sqlite:///sistema_nutricao.db
set SECRET_KEY=sistema-nutricao-secret-key

:: Iniciar o servidor
echo Iniciando servidor...
python -m flask run --host=0.0.0.0 --port=5000

pause
