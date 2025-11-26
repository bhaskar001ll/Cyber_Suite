import subprocess

def scan_wifi():
    try:
        result = subprocess.check_output(["nmcli", "dev", "wifi"], stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return "Error scanning WiFi: " + e.output.decode()