## 🚀 Feature: Wi-Fi Network Optimizer

### What this PR adds:
- **Automatic Wi-Fi scanning** using Windows `netsh` commands
- **Intelligent network selection** based on signal strength and user preferences  
- **Seamless connection switching** to optimize network performance
- **Comprehensive logging** and error handling
- **Configurable preferences** for network prioritization and blacklisting

### 🔧 Technical Implementation:
- **Scanner Module**: Discovers available networks and parses signal strength
- **Connector Module**: Manages network connections using existing profiles
- **Network Manager**: Orchestrates scanning and connection optimization
- **Configuration System**: Supports custom settings via JSON config files
- **Robust Error Handling**: Graceful handling of network failures and timeouts

### 🎛️ Key Features:
- ✅ Scans for known Wi-Fi networks with existing profiles
- ✅ Automatically connects to strongest available signal
- ✅ Respects user-defined preferred and blacklisted networks
- ✅ Prevents unnecessary switching (requires >10% signal improvement)
- ✅ Command-line interface with multiple operation modes
- ✅ Comprehensive logging with file and console output
- ✅ Zero external dependencies (uses only Python standard library)

### 🚦 Usage:
```bash
# Optimize connection (default)
python main.py

# Scan networks only  
python main.py --scan-only

# Check current status
python main.py --status

# Use custom config
python main.py --config config/settings.json --verbose
