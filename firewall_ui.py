import subprocess

def enable_firewall():
    subprocess.call(['sudo', 'ufw', 'enable'])

def disable_firewall():
    subprocess.call(['sudo', 'ufw', 'disable'])

def show_status():
    try:
        output = subprocess.check_output(['sudo', 'ufw', 'status'])
        return output.decode()
    except subprocess.CalledProcessError:
        return "Error getting firewall status"