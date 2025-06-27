@echo off
echo Executando testes de integração do Sistema de Nutrição...

:: Ativar ambiente virtual se não estiver ativado
if not defined VIRTUAL_ENV (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate
)

:: Instalar dependências necessárias para testes
echo Instalando dependências para testes...
pip install pytest pytest-flask pytest-cov

:: Executar testes com cobertura
echo Executando testes de integração com análise de cobertura...
python -m pytest tests\test_integracao.py -v

:: Verificar resultado dos testes
if %ERRORLEVEL% EQU 0 (
    echo ✅ Todos os testes passaram com sucesso!
) else (
    echo ❌ Alguns testes falharam. Verifique os erros acima.
)

pause
