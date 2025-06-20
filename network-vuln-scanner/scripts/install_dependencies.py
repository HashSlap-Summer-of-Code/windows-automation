#!/usr/bin/env python3
import subprocess
import sys
import os

def install_python_packages():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    
    requirements_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requirements.txt")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("✅ Python packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python packages: {e}")
        return False
    return True

def install_nmap():
    """Install nmap system package"""
    import platform
    system = platform.system().lower()
    
    print(f"Detected system: {system}")
    
    if system == "windows":
        print("📋 For Windows:")
        print("1. Download Nmap from: https://nmap.org/download.html")
        print("2. Install the Windows version")
        print("3. Add nmap to your system PATH")
        print("4. Restart your command prompt/PowerShell")
        
    elif system == "darwin":  # macOS
        print("Installing nmap on macOS...")
        try:
            # Try homebrew first
            subprocess.check_call(["brew", "install", "nmap"])
            print("✅ Nmap installed via Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Homebrew not found or failed")
            print("📋 Please install nmap manually:")
            print("1. Install Homebrew: https://brew.sh/")
            print("2. Run: brew install nmap")
            print("Or download from: https://nmap.org/download.html")
            
    elif system == "linux":
        print("Installing nmap on Linux...")
        try:
            # Try different package managers
            if subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0:
                subprocess.check_call(["sudo", "apt-get", "update"])
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "nmap"])
            elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
                subprocess.check_call(["sudo", "yum", "install", "-y", "nmap"])
            elif subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
                subprocess.check_call(["sudo", "dnf", "install", "-y", "nmap"])
            else:
                print("❌ No supported package manager found")
                print("📋 Please install nmap manually using your distribution's package manager")
                return False
            print("✅ Nmap installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install nmap: {e}")
            return False
    
    return True

def verify_installation():
    """Verify that all dependencies are properly installed"""
    print("\n🔍 Verifying installation...")
    
    # Check nmap
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Nmap is available")
        else:
            print("❌ Nmap not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ Nmap not found")
        return False
    
    # Check Python packages
    try:
        import nmap
        print("✅ python-nmap is available")
    except ImportError:
        print("❌ python-nmap not available")
        return False
    
    try:
        import schedule
        print("✅ schedule is available")
    except ImportError:
        print("❌ schedule not available")
        return False
    
    try:
        import jinja2
        print("✅ jinja2 is available")
    except ImportError:
        print("❌ jinja2 not available")
        return False
    
    print("✅ All dependencies verified successfully!")
    return True

def setup_directories():
    """Create necessary directories"""
    print("Setting up directory structure...")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    directories = [
        "reports/current",
        "reports/archive", 
        "logs",
        "templates"
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_config_files():
    """Create configuration files with default values"""
    print("Creating configuration files...")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Create email template
    from src.reporter import create_report_template
    create_report_template()
    print("✅ Created report template")
    
    # Create .env template
    env_template = """# Network Scanner Configuration
# Copy this file to .env and update with your settings

# Email Configuration
SCANNER_EMAIL_USER=your-email@gmail.com
SCANNER_EMAIL_PASSWORD=your-app-password

# SMTP Settings (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Network Settings
NETWORK_RANGES=192.168.1.0/24,192.168.0.0/24

# Alert Settings
ALERT_EMAIL=admin@yourdomain.com
"""
    
    env_path = os.path.join(base_dir, ".env.template")
    with open(env_path, "w") as f:
        f.write(env_template)
    print("✅ Created .env.template")

if __name__ == "__main__":
    print("🚀 Network Vulnerability Scanner - Installation Script")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Install system dependencies
    install_nmap()
    
    # Install Python packages
    if not install_python_packages():
        sys.exit(1)
    
    # Create config files
    create_config_files()
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Copy .env.template to .env and configure your settings")
        print("2. Run: python main.py --scan (for immediate scan)")
        print("3. Run: python scripts/setup_scheduler.py --create (to setup scheduled scans)")
    else:
        print("\n❌ Installation verification failed")
        sys.exit(1)