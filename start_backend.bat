@echo off
echo Starting ChatGPT UI Demo Backend...
cd /d "%~dp0backend"
echo Installing backend dependencies...
pip install -r requirements.txt
python app.py
pause 