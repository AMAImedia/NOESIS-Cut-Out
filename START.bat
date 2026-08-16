@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title NOESIS Cut-Out
set "PY=%~dp0vendor\python\python.exe"
if not exist "%PY%" goto missing_python
"%PY%" "%~dp0runtime\space_ports.py"
if errorlevel 1 goto check_failed
"%PY%" "%~dp0runtime\preflight.py"
if errorlevel 1 goto preflight_failed
echo NOESIS Cut-Out: http://127.0.0.1:8788
"%PY%" "%~dp0runtime\serve.py"
goto end
:missing_python
echo ERROR: vendor\python\python.exe is missing.
pause
exit /b 1
:check_failed
echo ERROR: disk or port preflight failed.
pause
exit /b 1
:preflight_failed
echo ERROR: integrity or dependency preflight failed.
pause
exit /b 1
:end
endlocal

