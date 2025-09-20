@echo off
echo ==========================
echo   Building Sysra Browser
echo ==========================

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Build with PyInstaller using spec file only
python -m PyInstaller --clean --noconfirm sysrabrowser.spec

echo ==========================
echo Build completed!
echo ==========================
pause
