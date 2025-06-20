#!/usr/bin/env python3
import sys
import argparse
import logging
from src.scanner import NetworkScanner
from src.reporter import ReportGenerator
from src.emailer import EmailNotifier
from src.scheduler import ScanScheduler

def main():
    parser = argparse.ArgumentParser(description="Network Vulnerability Scanner")
    parser.add_argument("--scan", action="store_true", help="Run immediate scan")
    parser.add_argument("--schedule", action="store_true", help="Start scheduler")
    parser.add_argument("--report-only", help="Generate report from existing scan file")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    if args.scan:
        run_scan()
    elif args.schedule:
        start_scheduler()
    elif args.report_only:
        generate_report_from_file(args.report_only)
    else:
        parser.print_help()

def run_scan():
    """Execute a complete network scan with reporting and notifications"""
    scanner = NetworkScanner()
    reporter = ReportGenerator()
    emailer = EmailNotifier()
    
    # Perform scan
    print("Starting network vulnerability scan...")
    results = scanner.scan_all_networks()
    
    # Save raw results
    results_file = scanner.save_results()
    
    # Generate reports
    summary = reporter.generate_summary_report(results)
    html_report = reporter.generate_html_report(results, summary)
    text_summary = reporter.generate_text_summary(summary)
    
    # Send email notification
    subject = f"Network Scan Complete - {summary['high_risk_findings']} High Risk Issues Found"
    emailer.send_report(subject, text_summary, html_report)
    
    print(f"Scan complete. Results saved to: {results_file}")
    print(f"HTML report: {html_report}")

def start_scheduler():
    """Start the scan scheduler"""
    scheduler = ScanScheduler(run_scan)
    scheduler.start_scheduler()
    
    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop_scheduler()
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()