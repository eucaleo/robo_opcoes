@echo off
setlocal

title Robo Opcoes - UI Moderna Dark

cd /d "%~dp0"

echo ================================================
echo Robo Opcoes - UI Moderna Dark
echo ================================================
echo.
echo Diretorio:
echo %CD%
echo.
echo Comando:
echo python -m UI.modern
echo.

if /I "%~1"=="--check" goto CHECK_ONLY

call :resolve_python
if errorlevel 1 goto FAIL

if not exist "UI\modern\__main__.py" (
    echo ERRO: UI\modern\__main__.py nao encontrado.
    echo.
    echo Este arquivo .cmd precisa ficar na raiz do projeto.
    goto FAIL
)

echo Iniciando sistema...
echo.

"%PY_EXE%" %PY_ARGS% -m UI.modern
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ================================================
echo Sistema encerrado com codigo: %EXIT_CODE%
echo ================================================
echo.
echo Pressione qualquer tecla para fechar.
pause >NUL

exit /b %EXIT_CODE%

:CHECK_ONLY
call :resolve_python
if errorlevel 1 exit /b 1

if not exist "UI\modern\__main__.py" (
    echo ERRO: UI\modern\__main__.py nao encontrado.
    exit /b 1
)

if not exist "UI\modern\app.py" (
    echo ERRO: UI\modern\app.py nao encontrado.
    exit /b 1
)

echo OK: iniciador validado.
echo Python selecionado: %PY_EXE% %PY_ARGS%
echo Comando usado: python -m UI.modern
exit /b 0

:resolve_python
set "PY_EXE="
set "PY_ARGS="

if exist ".venv\Scripts\python.exe" (
    set "PY_EXE=%CD%\.venv\Scripts\python.exe"
    set "PY_ARGS="
    exit /b 0
)

where python >NUL 2>&1
if not errorlevel 1 (
    set "PY_EXE=python"
    set "PY_ARGS="
    exit /b 0
)

where py >NUL 2>&1
if not errorlevel 1 (
    set "PY_EXE=py"
    set "PY_ARGS=-3"
    exit /b 0
)

echo ERRO: Python nao encontrado.
echo.
echo Tente rodar manualmente:
echo python -m UI.modern
echo.
echo Ou verifique se o Python esta instalado no PATH.
exit /b 1

:FAIL
echo.
echo Falha ao iniciar o sistema.
echo.
echo Pressione qualquer tecla para fechar.
pause >NUL
exit /b 1
