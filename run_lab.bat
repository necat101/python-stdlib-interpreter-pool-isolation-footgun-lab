@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

REM interpreter discovery: %PYTHON_BIN%, then python3.14, python3, python
set "PY="
if defined PYTHON_BIN (
    where /q "%PYTHON_BIN%"
    if !errorlevel! equ 0 set "PY=%PYTHON_BIN%"
)
if not defined PY (
    where /q python3.14
    if !errorlevel! equ 0 set "PY=python3.14"
)
if not defined PY (
    where /q python3
    if !errorlevel! equ 0 set "PY=python3"
)
if not defined PY (
    where /q python
    if !errorlevel! equ 0 set "PY=python"
)
if not defined PY (
    echo error: no python interpreter found ^(tried %%PYTHON_BIN%%, python3.14, python3, python^)
    exit /b 1
)

echo Using:
"%PY%" --version
echo.

echo ==^> syntax check
"%PY%" -m py_compile run_lab.py worker_tasks.py test_lab.py
if errorlevel 1 exit /b %errorlevel%
echo compile ok
echo.

echo ==^> run_lab
"%PY%" run_lab.py
if errorlevel 1 exit /b %errorlevel%
echo.

echo ==^> unittest
"%PY%" -m unittest -v
