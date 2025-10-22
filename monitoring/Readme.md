# 💽 diskmonitor.ps1 — C: Drive Disk Space Monitor

This PowerShell script continuously monitors free disk space on the `C:` drive and logs the result every 10 minutes. If the available space falls below **10 GB**, it triggers an alert in the terminal and logs the event.

---

## 📦 Features

- Checks free space on the `C:` drive.
- Logs every check to a file in the script's folder.
- Prints a warning if space drops below a 10 GB threshold.
- Runs indefinitely in a loop (can be stopped anytime).
- No external dependencies or tools required.

---

## 🛠️ Requirements

- **Windows 10 or higher**
- **PowerShell 5.1+** or **PowerShell Core 7+**
- No admin rights required

---

## 📄 How the Script Works

- It runs an infinite loop using `while ($true)`.
- Every cycle, it uses `Get-Volume` to check space on `C:`.
- The result is logged with a timestamp to `disk-monitor-log.txt` in the **same folder** as the script.
- If the space is **below 10 GB**, a warning is shown in yellow.

---

## 🔧 Configuration (Optional)

You can change these variables inside the script to adjust behavior:

```powershell
$DriveLetter     = "C"     # Which drive to monitor
$ThresholdGB     = 10      # Alert threshold in GB
$IntervalMinutes = 10      # Check frequency in minutes
```

---

## 🚀 How to Run

1. Open **PowerShell** (not CMD).
2. Navigate to the folder where the script is saved:

   ```powershell
   cd "C:\Path\To\Script"
   ```

3. (One-time) Allow script execution if not already enabled:

   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. Run the script:

   ```powershell
   .\diskmonitor.ps1
   ```

5. When prompted:
   ```
   Start monitoring now? (Y/N)
   ```
   ➤ Type `Y` and press Enter.

---

## 🛑 How to Stop It

- Press `Ctrl + C` in the PowerShell terminal.
- The script will exit and display:
  ```
  ⛔ Monitoring stopped by user.
  ```

---

## 📁 Log File

- Created in the **same folder** as the script.
- Named: `disk-monitor-log.txt`

Example entries:
```
2025-07-02 14:30:00 | Free space: 42.5 GB on drive C:
2025-07-02 15:30:00 | Free space: 9.8 GB on drive C:  << BELOW THRESHOLD!
```

---

## ❓ Common Questions

**Q: Will it monitor other drives?**  
Yes — change `$DriveLetter` in the script to `"D"`, `"E"`, etc.

**Q: Can I make it run only once?**  
Yes — replace the `while ($true)` loop with a single call and remove `Start-Sleep`.

**Q: Can I run this in the background or on boot?**  
Yes — use Windows Task Scheduler to run `powershell.exe -File "diskmonitor.ps1"` on startup.

---

## ✅ Good to Know

- The script is safe — it only reads disk space and writes logs.
- Does not delete files or change anything on your system.
- Logs grow slowly; consider archiving if used long-term.

---
