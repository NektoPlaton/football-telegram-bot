@echo off
REM --- Установка зависимостей ---
python -m pip install --upgrade pip
python -m pip install aiogram requests python-dotenv

REM --- Запуск бота ---
python main.py

pause
