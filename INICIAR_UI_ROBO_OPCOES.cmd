@echo off
setlocal

title Robo Opcoes - UI

cd /d "%~dp0"

echo ================================================
echo Robo Opcoes - Inicializador da UI
echo ================================================
echo.
echo Diretorio do projeto:
echo %CD%
echo.

if /I "%~1"=="--check" goto CHECK_ONLY

call :resolve_python
if errorlevel 1 goto FAIL

if not exist "main.py" (
    echo ERRO: main.py nao encontrado na raiz do projeto.
    echo Este acionador deve permanecer na raiz do repositorio.
    goto FAIL
)

echo Iniciando UI pelo entrypoint principal preservado:
echo python main.py
echo.

"%PY_EXE%" %PY_ARGS% main.py
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ================================================
echo UI encerrada com codigo: %EXIT_CODE%
echo ================================================
echo.
echo Pressione qualquer tecla para fechar esta janela.
pause >nul

exit /b %EXIT_CODE%

:CHECK_ONLY
call :resolve_python
if errorlevel 1 exit /b 1

if not exist "main.py" (
    echo ERRO: main.py nao encontrado.
    exit /b 1
)

echo OK: acionador validado.
echo Python selecionado: %PY_EXE% %PY_ARGS%
echo Entrypoint preservado: main.py
exit /b 0

:resolve_python
set "PY_EXE="
set "PY_ARGS="

if exist ".venv\Scripts\python.exe" (
    set "PY_EXE=%CD%\.venv\Scripts\python.exe"
    set "PY_ARGS="
    exit /b 0
)

where python >nul 2>nul
if not errorlevel 1 (
    set "PY_EXE=python"
    set "PY_ARGS="
    exit /b 0
)

where py >nul 2>nul
if not errorlevel 1 (
    set "PY_EXE=py"
    set "PY_ARGS=-3"
    exit /b 0
)

echo ERRO: Python nao encontrado.
echo Instale Python ou ative o ambiente virtual do projeto.
exit /b 1

:FAIL
echo.
echo Falha ao iniciar a UI.
echo Pressione qualquer tecla para fechar esta janela.
pause >nul
exit /b 1
