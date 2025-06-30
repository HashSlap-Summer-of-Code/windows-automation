"""
cpu-logger.py
-------------
This script monitors your computer's CPU usage every few seconds
and logs it to a text file. You can set the logging interval and
choose how long you want the logger to run.

Requirements:
- psutil (install with `pip install psutil`)
"""

import psutil           # To get CPU usage
import time             # To create delays
from datetime import datetime  # To add timestamps to the log

# -------------------------------
# Step 1: Welcome message
# -------------------------------
print("🧠 Welcome to the CPU Usage Logger!")
print("This script will monitor your CPU usage and save it to a text file.\n")

# -------------------------------
# Step 2: User inputs
# -------------------------------
# Ask the user how often to log (in seconds)
try:
    interval = float(input("⏱️  How many seconds between each check? (e.g., 5): "))
    duration = float(input("⏳  How many total seconds should the logger run? (e.g., 60): "))
except ValueError:
    print("⚠️ Invalid input. Please enter numbers only.")
    exit(1)

# -------------------------------
# Step 3: Setup log file
# -------------------------------
log_file = "cpu_log.txt"

try:
    with open(log_file, "a") as file:
        file.write("\n=== CPU Usage Log Started ===\n")
        file.write(f"Interval: {interval}s | Duration: {duration}s\n")

        print(f"\n🚀 Logging started... (Saving to {log_file})\nPress Ctrl+C to stop early.\n")

        # -------------------------------
        # Step 4: Logging loop
        # -------------------------------
        start_time = time.time()
        while True:
            current_time = time.time()

            # Check if we've reached the total duration
            if current_time - start_time >= duration:
                break

            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Write log entry
            log_entry = f"[{timestamp}] CPU Usage: {cpu_usage}%\n"
            file.write(log_entry)
            file.flush()  # Ensures data is written to file immediately

            print(log_entry.strip())  # Print to console for real-time feedback
            time.sleep(interval)

        print("\n✅ Logging finished. Check the cpu_log.txt file.")

except KeyboardInterrupt:
    print("\n🛑 Logging interrupted by user.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
