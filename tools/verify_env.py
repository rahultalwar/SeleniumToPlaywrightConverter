import sys
import subprocess
import urllib.request
import urllib.error

def check_python():
    print(f"Python version: {sys.version}")

def check_ollama():
    url = "http://localhost:11434"
    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                print("✅ Ollama is running.")
            else:
                print(f"⚠️ Ollama returned status code: {response.getcode()}")
    except urllib.error.URLError:
        print("❌ Ollama is NOT running on localhost:11434")
        print("   Please run 'ollama serve' in a terminal.")
    except ConnectionRefusedError:
        print("❌ Ollama Connection Refused")

def install_deps():
    packages = ["fastapi", "uvicorn", "requests", "pydantic"]
    print(f"Installing: {', '.join(packages)}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    check_python()
    install_deps()
    check_ollama()
