# 🧹 Browser Cleaner (Edge & Chrome) - PowerShell

This PowerShell script clears cache-related files for Microsoft Edge and Google Chrome across all detected user profiles. It supports interactive selection, confirms actions, warns if browsers are running, and provides a cleanup summary.

---

## 📦 Features

- Choose which browser(s) to clean: Edge, Chrome, or both
- Auto-detects user profiles (`Default`, `Profile 1`, etc.)
- Deletes:
  - `Cache`
  - `GPUCache`
  - `Code Cache`
- Warns if browser is currently running
- Asks for confirmation before deletion
- Outputs deleted file count and space reclaimed (in MB)
- Safe: does NOT delete cookies, history, or logins

---


## 🔧 Setup Instructions

1. **Clone the repository or copy the script manually**
   ```powershell
   git clone https://github.com/your-username/windows-automation.git
   cd windows-automation/browser-cleaner
   ```

2. **Open PowerShell as Administrator**


2. **Enable script execution for this session (Optional)**
    
    ```powershell
    
    Set-ExecutionPolicy RemoteSigned -Scope Process
    
    ```
    
3. **Run the script**
    
    ```powershell
    
    .\clear_browser_cache.ps1
    ```
    
4. **Follow the on-screen prompts**
    - Choose which browser(s) to clean
    - Confirm warnings if any browser is open
    - Review final summary (files deleted and MBs reclaimed)