@echo off
title FaceFinder Application
echo Starting FaceFinder...
timeout /t 1 /nobreak

REM Check if conda environment exists
call conda env list | find "facefinder" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo Error: facefinder environment not found!
    color 07
    timeout /t 4
    exit /b 1
)

REM Activate conda environment
call conda activate facefinder
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo Error: Failed to activate conda environment!
    color 07
    timeout /t 4
    exit /b 1
)

REM Run the main Python script
python src\main_windows.py
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo Error: Python script failed to execute!
    color 07
    timeout /t 4
    exit /b 1
)

echo FaceFinder completed successfully!
pause