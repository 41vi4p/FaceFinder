@echo off
REM Run with specific path
"%ProgramFiles%\CMake\bin\cmake.exe" --version
REM Execute with error checking
where cmake >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo CMake is installed
) else (
    echo Error! CMake is not installed. Please Install it Manually before Proceding...
    timeout /t 5
)

echo Checking Python installation...
where conda >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Python found:
    conda --version
    echo.
    echo Checking conda environment 'facefinder'...
    conda env list | find "facefinder" >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        @REM conda create -n facefinder python==3.9
        echo Environment 'facefinder' exists
        timeout /t 4
        conda activate facefinder
        timeout /t 2
        pip install -r requirements.txt

    ) else (
        echo Environment 'facefinder' not found!
        timeout /t 4
    )
) else (
    echo Error Python is not installed!!
    timeout /t 5
)

pause