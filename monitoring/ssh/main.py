from notifs.discord.discord import send_to_discord
from config import ssh_ban_duration, max_ssh_attempts, ssh_monitoring , ssh_notifications
import subprocess
import re
import threading

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
    try:
        result = subprocess.run(
            ["/usr/sbin/iptables", "-L", "INPUT", "-v", "-n", "--line-numbers"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        return ip in output
    except subprocess.CalledProcessError as e:
        send_to_discord(f"Error checking if IP ||{ip}|| is banned: {e}")
        return False

def ban_ip(ip):
    """
    Ban the specified IP address for SSH using iptables with a timeout and notify via Discord.

    Args:
        ip (str): IP address to be banned.
    """
    if ip == '::1':
        return
    try:
        subprocess.run(
            [
                "/usr/sbin/iptables", "-I", "INPUT", "-p", "tcp", "--dport", "22", "-s", ip, "-j", "DROP",
                "-m", "comment", "--comment", "ssh_attempts",
                "-m", "recent", "--name", "ssh_attempts", "--set"
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        send_to_discord(f"Error banning IP {ip}: {e}")
        return
    if ssh_notifications:
        send_to_discord(f"IP ||{ip}|| banned for {ssh_ban_duration} minutes due to SSH brute force attempts.")

    unban_thread = threading.Thread(target=unban_ip, args=(ip,), daemon=True)
    unban_thread.start()

def unban_ip(ip):
    """
    Remove the SSH ban on the specified IP address after the ban duration.

    Args:
        ip (str): IP address to be unbanned.
    """
    threading.Event().wait(ssh_ban_duration * 60)

    try:
        # Fetch current iptables rules with line numbers
        result = subprocess.run(
            ["/usr/sbin/iptables", "-L", "INPUT", "-v", "-n", "--line-numbers"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        
        # Find and remove the rule matching the banned IP
        for line in lines:
            if f"DROP" in line and ip in line and "ssh_attempts" in line:
                # Extract line number
                line_number = line.split()[0]
                # Delete the rule by line number
                subprocess.run(
                    ["/usr/sbin/iptables", "-D", "INPUT", line_number],
                    check=True
                )
                if ssh_notifications:

                    send_to_discord(f"IP ||{ip}|| has been unbanned after {ssh_ban_duration} minutes.")
                return
        
        send_to_discord(f"Error: IP ||{ip}|| was not found in the current iptables rules for unbanning.")

    except subprocess.CalledProcessError as e:
        send_to_discord(f"Error unbanning IP {ip}: {e}")
