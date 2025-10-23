"""
Launcher script for the Electronics Store Q&A Streamlit App
"""

import subprocess
import sys
import os


def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        "streamlit",
        "pandas",
        "chromadb",
        "sentence_transformers",
        "psycopg2",
        "sqlalchemy",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r streamlit_requirements.txt")
        return False

    return True


def main():
    """Main launcher function"""
    print("🚀 Electronics Store Q&A System Launcher")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print(
            "❌ main.py not found. Please run this script from the project root directory."
        )
        return

    # Check requirements
    print("🔍 Checking requirements...")
    if not check_requirements():
        return

    print("✅ All requirements satisfied!")

    # Check if vector embeddings exist
    if not os.path.exists("./chroma_db"):
        print("⚠️  Vector embeddings not found. They will be created on first run.")

    # Launch Streamlit
    print("\n🌐 Launching Streamlit app...")
    print("📱 The app will open in your default web browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "main.py",
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
                "--browser.gatherUsageStats",
                "false",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")


if __name__ == "__main__":
    main()
