# 🛡️ Defender Real-Time Protection Toggle Script

A PowerShell script to **enable or disable Windows Defender Real-Time Protection** interactively.  
Useful for automation, testing, or temporary performance boosts—**but use with care!**

---

## 🚨 IMPORTANT: READ THIS FIRST

- **Tamper Protection:**  
  Windows 10/11's Tamper Protection **must be disabled** for this script to work.  
  (You **cannot** turn off Tamper Protection via script—must be done manually.)
- **Administrator:**  
  The script must be run in an **elevated PowerShell window** (Run as Administrator).
- **Responsibility:**  
  Disabling Defender exposes you to malware/ransomware—**turn it back ON** after your work!
- **Exclusions Alternative:**  
  For most automation, simply **exclude your test folders** instead of disabling Defender entirely:
  ```powershell
  Add-MpPreference -ExclusionPath "C:\your\test\folder"
  ```

## 📄 What This Script Does

- Shows Defender’s current Real-Time Protection status.
- Prompts you to turn protection ON or OFF (or quit).
- Applies your choice.
- Confirms the new status.
- Checks both the preference flag and actual service state for maximum clarity.

---

