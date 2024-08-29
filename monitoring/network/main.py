import time
import psutil
import subprocess
from config import (bandwidth_threshold, threshold_monitoring, 
                    close_port_on_threshold_exceed, network_interface)
from notifs.discord.discord import send_to_discord

def monitor_bandwidth(interface=network_interface, threshold=bandwidth_threshold):
    if threshold_monitoring:
        try:
            net_before = psutil.net_io_counters(pernic=True).get(interface)
            if not net_before:
                return False

            time.sleep(1)  

            net_after = psutil.net_io_counters(pernic=True).get(interface)
            if not net_after:
                return False

            bytes_received = net_after.bytes_recv - net_before.bytes_recv
            bytes_sent = net_after.bytes_sent - net_before.bytes_sent

            total_bytes = bytes_received + bytes_sent
            if total_bytes > threshold:
                return True
        except Exception as e:
            print(f"Erreur lors de la surveillance de la bande passante: {e}")

    return False

def close_all_ports():
    if close_port_on_threshold_exceed:
        try:
            subprocess.run(["iptables", "-F"], check=True)
            send_to_discord("Tous les ports ont été fermés (self défense)")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la fermeture des ports: {e}")

def open_all_ports():
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-j", "ACCEPT"], check=True)
        print("Tous les ports ont été ouverts.")
        send_to_discord("Tous les ports ont été ouverts. (self défense)")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ouverture des ports: {e}")
 