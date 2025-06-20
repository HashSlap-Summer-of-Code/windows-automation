#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime

def create_windows_scheduled_task():
    """Create a Windows scheduled task for the network scanner"""
    
    # Get paths
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_exe = sys.executable
    script_path = os.path.join(current_dir, "scripts", "run_scan.py")
    
    # Task configuration
    task_name = "NetworkVulnerabilityScanner"
    
    # Create the scheduled task using schtasks command
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{python_exe}" "{script_path}"',
        "/sc", "weekly",
        "/d", "MON",
        "/st", "02:00",
        "/ru", "SYSTEM",
        "/f"  # Force create (overwrite if exists)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Successfully created scheduled task: {task_name}")
        print(f"   - Runs every Monday at 2:00 AM")
        print(f"   - Script: {script_path}")
        print(f"   - Python: {python_exe}")
        
        # Verify task was created
        verify_cmd = ["schtasks", "/query", "/tn", task_name]
        verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
        if verify_result.returncode == 0:
            print("✅ Task verification successful")
        else:
            print("⚠️  Task created but verification failed")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create scheduled task: {e}")
        print(f"Error output: {e.stderr}")
        print("\nTroubleshooting:")
        print("1. Run this script as Administrator")
        print("2. Ensure you have permission to create scheduled tasks")
        print("3. Check if the task name already exists")
        
    except FileNotFoundError:
        print("❌ schtasks command not found. This script requires Windows.")

def delete_scheduled_task():
    """Delete the scheduled task"""
    task_name = "NetworkVulnerabilityScanner"
    
    cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Successfully deleted scheduled task: {task_name}")
    except subprocess.CalledProcessError:
        print(f"⚠️  Task {task_name} not found or could not be deleted")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Windows scheduled task for network scanner")
    parser.add_argument("--create", action="store_true", help="Create scheduled task")
    parser.add_argument("--delete", action="store_true", help="Delete scheduled task")
    
    args = parser.parse_args()
    
    if args.create:
        create_windows_scheduled_task()
    elif args.delete:
        delete_scheduled_task()
    else:
        print("Use --create to create scheduled task or --delete to remove it")