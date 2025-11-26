# 🛡️ II Cyber Suite II v3

A powerful Python-based GUI application for ethical hacking and wireless security testing on Linux (Ubuntu). Built with `Tkinter`, it allows you to perform:

- 🔍 WiFi Scanning
- 🔥 Start/Stop Custom Packet Sniffing Firewall
- 🎯 Deauthentication Attacks
- 🔐 WPA/WPA2 Handshake Capture
- 🧠 Password Cracking using Wordlists
- 👻 Fluxion (Evil Twin Attack)
- 🛰️ Monitor Mode ON/OFF
- 🔚 One-click Exit with auto reset

> ⚠️ **This tool is for educational purposes only. Do not use it on any network or device without explicit permission.**

---

## 📁 Project Structure

cyber_suite/
├── ddos.py # (Optional/Deprecated)
├── firewall.py # Custom Scapy firewall (logs & blocks packets)
├── firewall_ui.py # Controls UFW firewall (legacy)
├── fproj/
│ └── fluxion/ # Cloned Fluxion tool
├── login.py # Login system using SQLite
├── main.py # Main GUI entry point
├── mitm_tools.py # MITM functions (monitor mode, attacks, etc.)
├── requirements.txt # Python dependencies
├── setup_db.py # Creates default admin login
├── wifi_scanner.py # WiFi list via nmcli
└── README.md # You're reading it!



---

## 🚀 Features

| Feature             | Description                                                       |
|---------------------|-------------------------------------------------------------------|
| **Login System**    | Username/password with SHA256 hash stored in SQLite              |
| **Firewall**        | Sniffs and blocks packets from blacklisted IPs/ports (Scapy)     |
| **WiFi Scanner**    | Lists nearby wireless networks via `nmcli`                        |
| **Fluxion**         | Launches Evil Twin attack script in new terminal                 |
| **Monitor Mode**    | Enables/disables monitor mode via `airmon-ng`                    |
| **Deauth Attack**   | Uses `aireplay-ng` to disconnect a victim from WiFi              |
| **Capture Handshake**| Uses `airodump-ng` to grab `.cap` file for WPA crack            |
| **Crack Handshake** | Uses `aircrack-ng` + wordlist to brute-force WPA password         |
| **GUI Inputs**      | BSSID, MAC, channel, wordlist + file pickers                     |
| **Exit Button**     | Safely shuts down app and resets adapter to managed mode         |

---

## 🔧 Installation

### 🐧 Ubuntu (Tested on 22.04+)

1. 📦 **Install system tools**:


sudo apt update
sudo apt install aircrack-ng xterm nmcli ufw python3-scapy gnome-terminal

2 🐍 Clone project and install Python dependencies:
cd ~
git clone https://github.com/yourname/cyber_suite.git
cd cyber_suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

   3 👤 Create default user:

python3 setup_db.py
# Login with:
# Username: admin
# Password: admin123

   4 🔓 Run GUI app with root:

sudo python3 main.py

