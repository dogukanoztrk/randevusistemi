import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

print("Diagnostic starting...")

try:
    import sqlalchemy
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
    print(f"SQLAlchemy file: {sqlalchemy.__file__}")
    from sqlalchemy.orm import Session
    print("Session import OK")
except Exception:
    print("SQLAlchemy import FAILED")
    traceback.print_exc()

try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
    from app.main import app
    print("FastAPI App import OK")
    
    import uvicorn
    print("Starting uvicorn...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
except Exception:
    print("FastAPI/Uvicorn/App import FAILED")
    traceback.print_exc()
