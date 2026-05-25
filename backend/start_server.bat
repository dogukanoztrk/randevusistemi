@echo off
set PYTHONPATH=%PYTHONPATH%;%CD%
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
pause
