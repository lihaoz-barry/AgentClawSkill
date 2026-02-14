"""
Installation Configuration Script
Verifies and configures all necessary dependencies
"""
import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_pip():
    """Check if pip is installed"""
    print("\nChecking pip...")
    try:
        import pip
        print(f"✅ pip is installed")
        return True
    except ImportError:
        print("❌ pip is not installed")
        return False


def install_dependencies():
    """Install Python dependencies from requirements.txt"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def install_playwright():
    """Install Playwright browsers"""
    print("\n🌐 Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False


def setup_environment():
    """Setup environment file"""
    print("\n📝 Setting up environment...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("⚠️  Please update .env with your settings")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✅ .env file already exists")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['data', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/ directory")
        else:
            print(f"✅ {directory}/ directory exists")
    return True


def verify_installation():
    """Verify installation by importing modules"""
    print("\n🔍 Verifying installation...")
    modules = ['flask', 'playwright', 'requests', 'bs4', 'schedule', 'dotenv', 'psutil']
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            all_ok = False
    
    return all_ok


def main():
    """Main installation configuration"""
    print("🚀 Job Search Automation System - Installation Configuration\n")
    print("=" * 60)
    
    steps = [
        ("Python Version", check_python_version),
        ("pip", check_pip),
        ("Dependencies", install_dependencies),
        ("Playwright", install_playwright),
        ("Environment", setup_environment),
        ("Directories", create_directories),
        ("Verification", verify_installation)
    ]
    
    all_passed = True
    for step_name, step_func in steps:
        print(f"\n{'=' * 60}")
        print(f"Step: {step_name}")
        print('=' * 60)
        if not step_func():
            all_passed = False
            print(f"⚠️  {step_name} step had issues")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ Installation configuration complete!")
        print("\nNext steps:")
        print("1. Update .env file with your settings")
        print("2. Run the application: python app.py")
        print("3. Open browser to: http://localhost:5000")
    else:
        print("⚠️  Installation had some issues. Please review the output above.")
    print("=" * 60)


if __name__ == '__main__':
    main()
