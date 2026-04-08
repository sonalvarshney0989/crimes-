#!/usr/bin/env python3
"""
Quick validation script for Crime Analytics Dashboard
"""

def test_imports():
    """Test if all required packages can be imported"""
    packages = [
        'streamlit',
        'pandas',
        'plotly',
        'folium',
        'streamlit_folium',
        'matplotlib',
        'seaborn'
    ]

    failed_imports = []

    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed_imports.append(package)

    return len(failed_imports) == 0

def test_data_files():
    """Test if data files exist"""
    import os

    files = [
        'clustered_crime_data.csv',
        'pca_crime_data.csv'
    ]

    missing_files = []

    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)

    return len(missing_files) == 0

def main():
    print("🔍 Crime Analytics Dashboard - Validation Check")
    print("=" * 50)

    print("\n📦 Testing imports...")
    imports_ok = test_imports()

    print("\n📁 Testing data files...")
    data_ok = test_data_files()

    print("\n" + "=" * 50)

    if imports_ok and data_ok:
        print("🎉 All checks passed! Your dashboard should work correctly.")
        print("\n🚀 Run with: streamlit run app3.py")
        return True
    else:
        print("⚠️  Some issues found. Please fix them before running the dashboard.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)