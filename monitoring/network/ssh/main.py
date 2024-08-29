from notifs.discord.discord import send_to_discord
from config import ssh_ban_duration, max_ssh_attempts, ssh_monitoring
import subprocess
import re

def monitor_ssh_failures():
    if ssh_monitoring:
        ip_failures = {}
        
        try:
            result = subprocess.run(
                ["journalctl", "-u", "ssh", "--since", "1 hour ago"],  
                capture_output=True,
                text=True,
                check=True
            )
            logs = result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la récupération des logs SSH: {e}")
            return {}

        for line in logs.splitlines():
            if "Failed password for" in line:
                match = re.search(r"Failed password for .* from (\S+)", line)
                if match:
                    ip = match.group(1)
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
        subprocess.run(
            ["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"],
            check=True
        )
        
        subprocess.run(
            ["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP", "-m", "comment", "recent ", "--name", "ssh_attempts", " --rcheck", "--seconds", str(ssh_ban_duration * 60)],
            check=True
        )
        
        send_to_discord(f"IP {ip} banned for {ssh_ban_duration} minutes due to SSH brute force attempts.")
    
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du bannissement de l'IP {ip}: {e}")
