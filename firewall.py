from scapy.all import *
import os
import time

from scapy.layers.inet import TCP, IP

# Define a list of blocked IP addresses (blacklist)
blocked_ips = ["192.168.1.5", "10.0.0.7", "192.168.137.1", "8.8.8.8", "31.13.64.51", "31.13.65.49", "157.240.14.60"]

# Block certain ports (e.g., HTTP port 80, SSH port 22)
blocked_ports = [80, 22, 443, 5222, 5223]

# Define the log file path in the same directory as the script
log_file_path = os.path.join(os.path.dirname(__file__), "packet_log.txt")


# Function to log packet details
def log_packet(action, packet):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{timestamp} - {action} - {packet.summary()}\n")


# Function to process each packet
def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst

        # Check if the packet is from or to a blacklisted IP
        if ip_src in blocked_ips or ip_dst in blocked_ips:
            print(f"Blocked packet from {ip_src} to {ip_dst}")
            log_packet("BLOCKED", packet)
            return  # Drop packet

        # Check if the packet is using a blocked port
        if TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport

            if sport in blocked_ports or dport in blocked_ports:
                print(f"Blocked packet from {ip_src}:{sport} to {ip_dst}:{dport}")
                log_packet("BLOCKED", packet)
                return  # Drop packet

    # Log allowed packets
    print(f"Allowed packet: {packet.summary()}")
    log_packet("ALLOWED", packet)


# Enable IP forwarding on Linux (optional)
def enable_ip_forwarding():
    if os.name == 'posix':  # Linux/Unix-like systems only
        try:
            with open("/proc/sys/net/ipv4/ip_forward", 'w') as f:
                f.write('1')
            print("IP Forwarding enabled")
        except PermissionError:
            print("Permission denied: Run script with elevated privileges to enable IP forwarding")


# Disable IP forwarding (optional)
def disable_ip_forwarding():
    if os.name == 'posix':
        try:
            with open("/proc/sys/net/ipv4/ip_forward", 'w') as f:
                f.write('0')
            print("IP Forwarding disabled")
        except PermissionError:
            print("Permission denied: Run script with elevated privileges to disable IP forwarding")


if __name__ == "__main__":
    # Enable IP forwarding for routing (optional)
    enable_ip_forwarding()

    # Start packet sniffing with filtering logic
    print("Starting firewall with logging...")
    sniff(prn=packet_callback, store=0)  # Start packet sniffing

    # Disable IP forwarding when done (optional)
    disable_ip_forwarding()

