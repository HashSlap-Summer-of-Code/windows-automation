import schedule
import time
import threading
import logging
from datetime import datetime
from typing import Callable
from config.settings import *

class ScanScheduler:
    def __init__(self, scan_function: Callable):
        self.scan_function = scan_function
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler_thread = None
        
    def setup_schedule(self):
        """Setup the scanning schedule"""
        if SCAN_SCHEDULE == "weekly":
            getattr(schedule.every(), SCAN_DAY.lower()).at(SCAN_TIME).do(self._run_scheduled_scan)
            self.logger.info(f"Scheduled weekly scan on {SCAN_DAY} at {SCAN_TIME}")
        elif SCAN_SCHEDULE == "daily":
            schedule.every().day.at(SCAN_TIME).do(self._run_scheduled_scan)
            self.logger.info(f"Scheduled daily scan at {SCAN_TIME}")
        else:
            self.logger.warning(f"Unknown schedule type: {SCAN_SCHEDULE}")
    
    def _run_scheduled_scan(self):
        """Execute the scheduled scan"""
        self.logger.info("Starting scheduled network scan")
        try:
            self.scan_function()
            self.logger.info("Scheduled scan completed successfully")
        except Exception as e:
            self.logger.error(f"Scheduled scan failed: {str(e)}")
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            self.logger.warning("Scheduler already running")
            return
        
        self.setup_schedule()
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        self.logger.info("Scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_immediate_scan(self):
        """Run an immediate scan"""
        self.logger.info("Running immediate network scan")
        self._run_scheduled_scan()

# Windows Task Scheduler integration
def create_windows_task():
    """Create Windows Task Scheduler entry"""
    import subprocess
    import sys
    
    script_path = os.path.abspath("scripts/run_scan.py")
    python_path = sys.executable
    
    # Create task XML
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <WeeklyTrigger>
      <DaysOfWeek>
        <Monday />
      </DaysOfWeek>
      <StartBoundary>2024-01-01T02:00:00</StartBoundary>
    </WeeklyTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>{python_path}</Command>
      <Arguments>{script_path}</Arguments>
      <WorkingDirectory>{os.getcwd()}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    
    # Save task XML
    with open("task.xml", "w") as f:
        f.write(task_xml)
    
    # Create task using schtasks
    try:
        subprocess.run([
            "schtasks", "/create", "/tn", "NetworkVulnScanner",
            "/xml", "task.xml", "/f"
        ], check=True)
        print("Windows Task Scheduler entry created successfully")
        os.remove("task.xml")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Windows task: {e}")