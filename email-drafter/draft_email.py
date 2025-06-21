"""
Automates Outlook to create a new email draft with predefined subject and body.
Requires: Outlook to be installed and signed in.
Run with: python draft_email.py
"""

import pyautogui
import time
import subprocess

# Delay to let you switch windows if needed
print("Starting Outlook...")
subprocess.Popen(["start", "outlook"], shell=True)
time.sleep(8)  # Wait for Outlook to open

# Create a new email
pyautogui.hotkey('ctrl', 'n')  # Open new email
time.sleep(2)

# Type subject
pyautogui.press('tab')  # Move to Subject field
subject = "Meeting Follow-Up"
pyautogui.write(subject, interval=0.05)

# Move to body
pyautogui.press('tab')
body = "Details at 02:30 PM IST"
pyautogui.write(body, interval=0.05)

# Save as draft
pyautogui.hotkey('ctrl', 's')  # Save email as draft
time.sleep(1)

print("Draft saved successfully!")

