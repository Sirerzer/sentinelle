from notifs.discord.discord import send_to_discord
from config import ssh_ban_duration, max_ssh_attempts, ssh_monitoring , banned_ips
import subprocess
import re
import threading
import time

def monitor_ssh_failures():
    if not ssh_monitoring:
        return {}

    ip_failures = {}

    result = subprocess.run(
        ["journalctl", "-u", "ssh", "--since", "1 hour ago"],
        capture_output=True,
        text=True,
        check=True
    )
    logs = result.stdout

    for line in logs.splitlines():
        if "Failed password for" in line:
            match = re.search(r"Failed password for .* from (\S+)", line)
            if match:
                ip = match.group(1)
                ip_failures[ip] = ip_failures.get(ip, 0) + 1
                if ip_failures[ip] >= max_ssh_attempts:
                    if not is_ip_banned(ip):
                        ban_ip(ip)
                        ip_failures[ip] = 0

    return ip_failures

def is_ip_banned(ip):
    """
    Check if the specified IP address is currently banned.
    
    Args:
        ip (str): IP address to check.
        
    Returns:
        bool: True if the IP is banned, False otherwise.
    """
    return banned_ips.get(ip, False)

def ban_ip(ip):
    """
    Ban the specified IP address for SSH by killing active SSH sessions and notify via Discord.
    
    Args:
        ip (str): IP address to be banned.
    """
    try:
        kill_ssh_sessions(ip)
    except Exception as e:
        send_to_discord(f"Error banning IP {ip}: {e}")
        return

    banned_ips[ip] = True

    send_to_discord(f"IP ||{ip}|| banned for {ssh_ban_duration} minutes due to SSH brute force attempts.")

    unban_thread = threading.Thread(target=unban_ip, args=(ip,), daemon=True)
    unban_thread.start()

def kill_ssh_sessions(ip):
    """
    Kill existing SSH sessions from the specified IP address.
    
    Args:
        ip (str): IP address to check for active SSH sessions.
    """
    try:
        result = subprocess.run(
            ["ss", "-o", "state", "established", "sport", "22"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        for line in output.splitlines():
            if ip in line:
                pid_match = re.search(r"pid=(\d+)", line)
                if pid_match:
                    pid = pid_match.group(1)
                    subprocess.run(["kill", "-9", pid], check=True)
                    send_to_discord(f"Killed SSH session with PID {pid} from IP {ip}.")
    except subprocess.CalledProcessError as e:
        send_to_discord(f"Error killing SSH sessions for IP {ip}: {e}")

def unban_ip(ip):
    """
    Continuously kill SSH sessions from the banned IP address until the ban duration expires.
    
    Args:
        ip (str): IP address to be unbanned.
    """
    end_time = time.time() + ssh_ban_duration * 60

    while time.time() < end_time:
        kill_ssh_sessions(ip)  
        
    banned_ips[ip] = False
    send_to_discord(f"IP ||{ip}|| has been unbanned after {ssh_ban_duration} minutes.")

