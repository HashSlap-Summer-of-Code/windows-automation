# 📶 Wi-Fi Auto Connect Optimizer (Windows)

This Python script helps you automatically connect to the **strongest known Wi-Fi network** available on your Windows machine using native `netsh` commands.

---

## 📌 Features

- Scans nearby Wi-Fi networks and their signal strengths
- Matches available SSIDs against your saved network profiles
- Connects to the one with the **strongest signal**
- Uses only built-in Windows tools (`netsh`) via `subprocess`

---

## 🖥️ Requirements

- Windows OS
- Python 3.x installed
- Previously saved Wi-Fi profiles (i.e., networks you've connected to before)

---

## 🚀 Usage

```bash
python wifi-auto-connect.py
