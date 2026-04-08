#!/usr/bin/env python3
"""
Crime Analytics Dashboard Launcher
================================

This script helps you launch the Crime Analytics Dashboard with proper setup.

Usage:
    python run_dashboard.py

Or make it executable and run:
    chmod +x run_dashboard.py
    ./run_dashboard.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'folium',
        'streamlit_folium'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n📦 Install with: pip install -r requirements.txt")
        return False

    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'clustered_crime_data.csv',
        'pca_crime_data.csv'
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print("❌ Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n📁 Please ensure all data files are in the current directory.")
        return False

    return True

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting Crime Analytics Dashboard...")
    print("📱 App will be available at: http://localhost:8501")
    print("❌ Press Ctrl+C to stop the application\n")

    try:
        # Run streamlit with the main app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            'app3.py',
            '--server.headless', 'true',
            '--server.address', '0.0.0.0'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        return False

    return True

def main():
    """Main launcher function"""
    print("🚔 Crime Analytics Dashboard Launcher")
    print("=" * 40)

    # Check requirements
    if not check_requirements():
        return False

    # Check data files
    if not check_data_files():
        return False

    # Run the application
    success = run_streamlit()

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)