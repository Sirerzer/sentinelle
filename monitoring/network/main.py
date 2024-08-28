import time
import psutil
import subprocess
from config import threshold , threshold_monitoring , close_port , interface
from notifs.discord.discord import send_to_discord

def monitor_bandwidth(interface=interface, threshold=threshold): 
    if threshold_monitoring:
        try:
            net_before = psutil.net_if_addrs().get(interface)
            if not net_before:
                return False

            time.sleep(1)  
            net_after = psutil.net_if_addrs().get(interface)
            if not net_after:
                return False

            bytes_received = net_after[0].address - net_before[0].address
            bytes_sent = net_after[1].address - net_before[1].address

            total_bytes = bytes_received + bytes_sent
            if total_bytes > threshold:
                return True
        except Exception as e:
            print(f"Erreur lors de la surveillance de la bande passante: {e}")

        return False

def close_all_ports():
    if close_port:
        try:

            subprocess.run(["iptables", "-F"], check=True)

            send_to_discord("Tout les ports on éte ferme (self deffensse)")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la fermeture des ports: {e}")

def open_all_ports():
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-j", "ACCEPT"], check=True)
        print("Tous les ports ont été ouverts.")
       
        send_to_discord("Tous les ports ont été ouverts. (self deffensse)")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ouverture des ports: {e}")
