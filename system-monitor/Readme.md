# 🧠 CPU Usage Logger

Logs your system's CPU usage every N seconds and saves the results in a file called `cpu_log.txt`.

## ✨ Features

- ⏱ Interactive: Set custom logging intervals and total duration
- 📄 Logs timestamped CPU usage to `cpu_log.txt`
- 📦 Minimal dependencies (only `psutil`)
- 👶 Beginner-friendly: fully commented and easy to understand
- 🔒 Graceful exit on `Ctrl+C` with message
- 💻 Cross-platform support (Windows, macOS, Linux)

## 🛠 Setup Instructions

### 1. Create and activate a virtual environment

```bash
cd system-monitor
```
```
python -m venv venv
```

```
venv\Scripts\activate      # On Windows 
```

```
source venv/bin/activate   # On macOS/Linux
```

### ✅ 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt` contains:
> ```
> psutil==5.9.6
> ```

---

## 🚀 Running the Script

Run the script using:

```bash
python cpu-logger.py
```

Then follow the prompts:
- `⏱️  How many seconds between each check? (e.g., 5):`
- `⏳  How many total seconds should the logger run? (e.g., 60):`

The script will log real-time CPU usage to a file like:

```text
[2025-06-30 14:25:01] CPU Usage: 17.0%
[2025-06-30 14:25:06] CPU Usage: 22.3%
```

Press `Ctrl + C` at any time to stop early.

---

## 📁 Output

All logs will be saved to:
```
cpu_log.txt
```

This file is created automatically in the same folder.

---

## 🧼 Cleanup

To remove the virtual environment and logs:

```bash
deactivate          # Exit venv
rm -r venv          # macOS/Linux
rmdir /S /Q venv    # Windows
del cpu_log.txt
```
