import sys
import subprocess
import os

# Load environment variables from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def check_python():
    print(f"Python version: {sys.version}")

def check_k2_api():
    """Check if K2 API key is configured."""
    api_key = os.getenv("K2_API_KEY")
    if api_key:
        # Mask the key for display
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✅ K2_API_KEY is set ({masked_key})")
        return True
    else:
        print("❌ K2_API_KEY is NOT set")
        print("   Please create a .env file with your K2 API key:")
        print("   K2_API_KEY=your_api_key_here")
        return False

def check_k2_connection():
    """Test connectivity to K2 API."""
    import urllib.request
    import urllib.error
    
    api_url = os.getenv("K2_API_URL", "https://api.k2.ai/v1/chat/completions")
    # Just check if the domain is reachable
    try:
        from urllib.parse import urlparse
        parsed = urlparse(api_url)
        test_url = f"{parsed.scheme}://{parsed.netloc}"
        
        req = urllib.request.Request(test_url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"✅ K2 API endpoint is reachable ({test_url})")
    except urllib.error.URLError as e:
        print(f"⚠️  Could not reach K2 API endpoint: {e}")
        print("   The API will be tested when you make your first conversion request.")
    except Exception as e:
        print(f"⚠️  Connectivity check skipped: {e}")

def install_deps():
    packages = ["fastapi", "uvicorn", "requests", "pydantic", "python-dotenv"]
    print(f"Installing: {', '.join(packages)}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        sys.exit(1)

def create_env_template():
    """Create a .env template file if it doesn't exist."""
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write("# K2 API Configuration\n")
            f.write("K2_API_KEY=your_k2_api_key_here\n")
            f.write("K2_API_URL=https://api.k2.ai/v1/chat/completions\n")
            f.write("K2_MODEL=k2-thinking\n")
        print("📝 Created .env template file. Please edit it with your actual K2 API key.")

if __name__ == "__main__":
    print("=" * 50)
    print("BlastConvert Environment Verification")
    print("=" * 50)
    
    check_python()
    install_deps()
    
    print("\n" + "-" * 50)
    print("Checking K2 API Configuration")
    print("-" * 50)
    
    create_env_template()
    api_configured = check_k2_api()
    check_k2_connection()
    
    if not api_configured:
        print("\n⚠️  WARNING: K2_API_KEY is not configured!")
        print("   The converter will not work until you set your API key.")
        sys.exit(1)
    else:
        print("\n✅ Environment verification complete!")
        print("   You can now run the converter with: ./run.sh")
