@echo off
echo Downloading Miniconda3...




echo Download complete.
echo Installing Miniconda3...

@REM :: Silent installation of Miniconda3
@REM %OUTPUT% /InstallationType=JustMe /RegisterPython=0 /AddToPath=1 /S /D=%USERPROFILE%\Miniconda3

echo Installation complete.


echo Conda environment 'facefinder' created.

@REM CMake install
echo Installing CMake... Follow the instructions on the Window.
@REM win_installer_files\cmake-3.31.4-windows-x86_64.msi

@REM Install Visual Studio Community
echo Installing Visual Studio Community... Follow the instructions on the Window.
echo Install the 'Desktop Development with C++' Package on the Open Window
timeout /t 5
win_installer_files\VisualStudioSetup.exe
echo Done Installing 'Desktop Development with C++' from Visual Studio Community


pause
