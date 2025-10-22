#!/usr/bin/env python3

"""
Wi-Fi Auto Connect Optimizer (Windows)

Scans available networks, checks signal strengths,
and auto-connects to the strongest known Wi-Fi network.

Usage:
    python wifi-auto-connect.py

Requirements:
    - Windows OS
    - Python 3.x
    - Must have previously connected to target networks (profiles must exist)
"""

import subprocess
import re

def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout

def parse_networks(raw_output):
    networks = []
    current_ssid = None

    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("SSID") and ":" in line:
            current_ssid = line.split(":", 1)[1].strip()
        elif line.startswith("Signal") and current_ssid:
            signal_str = line.split(":", 1)[1].strip().replace('%', '')
            try:
                signal = int(signal_str)
                networks.append((current_ssid, signal))
            except ValueError:
                pass
            current_ssid = None

    return networks

def get_saved_profiles():
    output = run_command("netsh wlan show profiles")
    return re.findall(r"All User Profile\s*:\s(.*)", output)

def connect_to_network(ssid):
    print(f"[i] Attempting to connect to '{ssid}'...")
    result = run_command(f'netsh wlan connect name="{ssid}"')
    if "completed successfully" in result:
        print(f"[✓] Connected to '{ssid}'")
    else:
        print(f"[!] Failed to connect to '{ssid}'")
        print(result)

def main():
    print("📡 Scanning for available Wi-Fi networks...")
    scan_output = run_command("netsh wlan show networks mode=bssid")
    available = parse_networks(scan_output)
    if not available:
        print("[!] No Wi-Fi networks detected.")
        return

    saved_profiles = get_saved_profiles()
    known_networks = [(ssid, signal) for ssid, signal in available if ssid in saved_profiles]

    if not known_networks:
        print("[!] No known networks are available to connect.")
        return

    best_ssid, best_signal = max(known_networks, key=lambda x: x[1])
    print(f"📶 Best known network: '{best_ssid}' with signal {best_signal}%")
    connect_to_network(best_ssid)

if __name__ == "__main__":
    main()
