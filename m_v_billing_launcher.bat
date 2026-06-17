@echo off
title M.V. Billing Control Panel
color 0A

:: REPLACE THIS PATH WITH THE REAL FOLDER LOCATION OF manage.py
cd "D:\Computer Science\Project\Personal"

echo Starting M.V. Billing Server...

:: Start the server silently in the background
start /B python manage.py runserver > NUL 2>&1

:: Wait 3 seconds for it to boot up
timeout /t 3 /nobreak > NUL

:: Open Google Chrome App
start chrome.exe --app="http://127.0.0.1:8000"

cls
echo ==========================================================
echo                  SYSTEM IS RUNNING!
echo ==========================================================
echo.
echo   The M.V. Billing app is now open in Chrome.
echo.
echo   IMPORTANT: Keep this black window open!
echo   When you are finished billing for the day,
echo   PRESS ANY KEY in this window to safely stop the server.
echo.
echo ==========================================================
pause

:: When a key is pressed, force kill the background Python server
taskkill /IM python.exe /F > NUL 2>&1
exit