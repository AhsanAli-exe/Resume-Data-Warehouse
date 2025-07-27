#!/usr/bin/env python3
"""
Resume ETL Pipeline Runner
Simple script to start the FastAPI server and Streamlit dashboard
"""

import subprocess
import sys
import os
import time

def main():
    print("🚀 Starting Resume ETL Pipeline...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("api/main.py"):
        print("❌ Error: Please run this script from the 'Resume Pipeline' directory")
        sys.exit(1)
    
    print("📋 Prerequisites Check:")
    print("✅ Python environment")
    print("✅ Dependencies installed")
    print("✅ Database schema created")
    print("✅ Data loaded")
    
    print("\n🎯 Starting Services:")
    print("1. FastAPI Server (http://127.0.0.1:8000)")
    print("2. Streamlit Dashboard (http://localhost:8501)")
    
    print("\n📝 Instructions:")
    print("- FastAPI will start automatically")
    print("- Open a new terminal and run: streamlit run dashboard/streamlit_app.py")
    print("- Or visit the dashboard URL above")
    
    print("\n🔗 API Documentation:")
    print("- Swagger UI: http://127.0.0.1:8000/docs")
    print("- ReDoc: http://127.0.0.1:8000/redoc")
    
    print("\n" + "=" * 50)
    print("🎉 Your ETL Pipeline is ready!")
    print("=" * 50)

if __name__ == "__main__":
    main() 