@echo off
echo Iniciando Sistema de Nutricao (Versao Completa)...

:: Ativar ambiente virtual se não estiver ativado
if not defined VIRTUAL_ENV (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate
)

:: Instalar dependências
echo Instalando dependencias...
pip install flask flask-sqlalchemy flask-login flask-cors

:: Definir variáveis de ambiente
set FLASK_APP=backend
set FLASK_ENV=development
set DATABASE_URL=sqlite:///sistema_nutricao.db
set SECRET_KEY=sistema-nutricao-secret-key

:: Iniciar o servidor com o app.py corrigido
echo Iniciando servidor...
python app.py

pause
