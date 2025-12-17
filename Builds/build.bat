@echo off
REM Clean old build/dist folders
rmdir /s /q build
rmdir /s /q dist

REM Activate your virtual environment
call .venv\Scripts\activate

REM Run PyInstaller with proper flags
pyinstaller --onefile --windowed --icon=app.ico --hidden-import=mysql.connector main.py

REM Pause so you can see any errors
pause