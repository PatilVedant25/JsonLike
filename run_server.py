"""
Server Launcher Script for AI-Powered Product Intelligence Platform.
"""
import os
import sys

# Ensure UTF-8 output encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uvicorn

if __name__ == "__main__":
    # Ensure backend directory is in python path
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
        
    print("==========================================================================")
    print("Launching AI-Powered Product Intelligence Platform (UniCat 2.0)")
    print("Web Application & Interactive Workbench: http://127.0.0.1:8000")
    print("Swagger REST API Documentation: http://127.0.0.1:8000/docs")
    print("==========================================================================")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
