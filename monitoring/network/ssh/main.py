from ....notifs.discord.discord import send_to_discord
from ....config import ssh_ban_duration ,  max_ssh_attempts , ssh
import subprocess

def monitor_ssh_failures():
    if ssh:
        log_path="/var/log/auth.log"
        ip_failures = {}
        with open(log_path, "r") as log_file:
            lines = log_file.readlines()
        
        for line in lines:
            if "Failed password for" in line:
                parts = line.split()
                if len(parts) >= 11:
                    ip = parts[10]
                    if ip not in ip_failures:
                        ip_failures[ip] = 0
                    ip_failures[ip] += 1
                    if ip_failures[ip] >= max_ssh_attempts:
                        ban_ip(ip)
                        ip_failures[ip] = 0  
        return ip_failures

def ban_ip(ip):
    """
    Ban the specified IP address using iptables with a timeout and notify via Discord.

    Args:
        ip (str): IP address to be banned.
    """
    try:
        subprocess.run([
            "iptables", "-I", "INPUT", "-s", ip, "-j", "REJECT", "--reject-with", "icmp-host-prohibited"
        ], check=True)
        
        subprocess.run([
            "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP", "-m", "comment", "--comment", "temporary ban", "-m", "recent", "--name", "ssh_attempts", "--set", "--seconds", str(ssh_ban_duration * 60)
        ], check=True)
        
        # Send a notification to Discord
        send_to_discord(f"IP {ip} banned for {ssh_ban_duration} minutes due to SSH brute force attempts.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error banning IP {ip}: {e}")