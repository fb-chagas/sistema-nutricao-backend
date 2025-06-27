@echo off
echo Iniciando Sistema de Nutrição (Versão Simplificada)...

:: Ativar ambiente virtual se não estiver ativado
if not defined VIRTUAL_ENV (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate
)

:: Iniciar o servidor diretamente
echo Iniciando servidor...
python app.py

pause
