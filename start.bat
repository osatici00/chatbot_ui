@echo off
echo Starting ChatGPT UI Demo...
echo.

echo Installing dependencies...
echo.

echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo Installing backend dependencies...
cd ..\backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo Starting services...
echo.

echo Starting backend server on port 8001...
start "Backend API" cmd /k "python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak

echo Starting frontend server on port 3000...
cd ..\frontend
start "Frontend Dev Server" cmd /k "npm run dev"

echo.
echo =====================================================
echo   ChatGPT UI Demo is starting...
echo   Backend:  http://localhost:8001
echo   Frontend: http://localhost:3000
echo =====================================================
echo.
echo Press any key to open browser...
pause
start http://localhost:3000 