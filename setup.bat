@echo off
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
python manage.py migrate
python manage.py create_initial_admin
echo.
echo Projeto preparado.
echo Execute: run.bat
