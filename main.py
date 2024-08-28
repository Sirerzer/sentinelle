import psutil
import os
import time
import zipfile
import glob
import shutil
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import subprocess
from datetime import datetime

RAM_THRESHOLD = 99  
CPU_THRESHOLD = 99 

minecraft_indicators = [
    'net/minecraft/server/',
    'org/bukkit/',
    'com/destroystokyo/paper/',
    'com/velocitypowered/api/',
    'io/papermc/paper/',
    'META-INF/maven/org.spigotmc/spigot-api/',
    'net/md_5/bungee/',
    'io/papermc/paperclip',
    "org/bukkit/craftbukkit",
    "net/minecraftforge",
]

def get_top_process():
    processes = [(proc, proc.memory_percent(), proc.cpu_percent(interval=0.1))
                 for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent'])]
    processes.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return processes[0][0] if processes else None

def kill_process(proc):
    try:
        print(f"Termination du processus: {proc.name()} (PID: {proc.pid})")
        proc.terminate()
        proc.wait(timeout=3)
    except psutil.NoSuchProcess:
        print("Processus déjà terminé.")

def is_minecraft_server_jar(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            for file_name in jar.namelist():
                if any(indicator in file_name for indicator in minecraft_indicators):
                    return True
        return False
    except:
        pass

def send_to_discord(message, webhook_url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="Notification", description=message, color=0xff0000)
    webhook.add_embed(embed)
    webhook.execute()

def is_file_being_uploaded(file_path, wait_time=1):
    try:
        initial_size = os.path.getsize(file_path)
        time.sleep(0.1)
        final_size = os.path.getsize(file_path)
        return initial_size != final_size
    except:
        return True

def move_large_file(file_path, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    dest_path = os.path.join(destination_folder, os.path.basename(file_path))
    shutil.move(file_path, dest_path)
    return dest_path

def get_server_id_from_uuid(uuid, api_url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    page = 1
    while True:
        servers_url = f"{api_url}/api/application/servers?page={page}"
        try:
            response = requests.get(servers_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve servers: {e}")
            return None

        data = response.json()
        servers = data.get('data', [])

        if not servers:
            print("No server found with the specified UUID.")
            return None

        for server in servers:
            if server['attributes'].get('uuid') == uuid:
                return server['attributes'].get('id')

        page += 1
        if page > data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
            print("No server found with the specified UUID.")
            return None

def suspend_pterodactyl_server(server_id, api_url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    suspend_url = f"{api_url}/api/application/servers/{server_id}/suspend"
    response = requests.post(suspend_url, headers=headers)
    return response.status_code == 204 

def search_and_clean_jars(base_path, webhook_url, api_url, api_key):
    jar_paths = glob.glob(os.path.join(base_path, '*/*.jar'))
    for jar_path in jar_paths:
        uuid = os.path.basename(os.path.dirname(jar_path))
        short_uuid = uuid
        print(short_uuid)
        if is_file_being_uploaded(jar_path):
            print(f"File is still uploading: {jar_path}")
            continue
        
        if not is_minecraft_server_jar(jar_path):
            print(f"Non-Minecraft JAR detected: {jar_path}")
            file_size_mb = os.path.getsize(jar_path) / (1024 * 1024)
            
            if file_size_mb > 8:  
                new_path = move_large_file(jar_path, f"/var/sentinelle/{uuid}")
                send_to_discord(f"File moved to: {new_path}", webhook_url)
            else:
                send_to_discord(f"Non-Minecraft JAR detected and sent: {jar_path}", webhook_url)
                with open(jar_path, "rb") as f:
                    webhook = DiscordWebhook(url=webhook_url)
                    webhook.add_file(file=f.read(), filename=os.path.basename(jar_path))
                    webhook.execute()
                os.remove(jar_path)
            
            server_id = get_server_id_from_uuid(short_uuid, api_url, api_key)
            print(server_id)
            if server_id:
                if suspend_pterodactyl_server(server_id, api_url, api_key):
                    print(f"Server {short_uuid} suspended successfully.")
                    send_to_discord(f"Server {short_uuid} suspended due to suspicious JAR file.", webhook_url)
                else:
                    print(f"Failed to suspend server {short_uuid}.")
            else:
                print(f"Server ID not found for UUID: {short_uuid}")
            break

def monitor_bandwidth(interface="eth0", threshold=100000000):  # 100 MB/s comme seuil d'exemple
    try:
        net_before = psutil.net_if_addrs().get(interface)
        if not net_before:
            return False
        
        time.sleep(1)  # Attendre 1 seconde pour mesurer le débit
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
    try:
        subprocess.run(["iptables", "-F"], check=True)  # Fermer tous les ports
        send_to_discord("Tout les ports on éte ferme (self deffensse)", webhook_url)

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la fermeture des ports: {e}")

def open_all_ports():
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-j", "ACCEPT"], check=True)  # Ouvrir tous les ports
        print("Tous les ports ont été ouverts.")
        send_to_discord("Tous les ports ont été ouverts. (self deffensse)", webhook_url)

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ouverture des ports: {e}")


def monitor_ssh_failures(log_path="/var/log/auth.log"):
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
                if ip_failures[ip] >= 5:
                    ban_ip(ip)
                    ip_failures[ip] = 0  
    return ip_failures

def ban_ip(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        send_to_discord(f"IP {ip} banned for 1 hour due to SSH brute force attempts.", webhook_url)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du bannissement de l'IP {ip}: {e}")

webhook_url = ""
base_path = "/var/lib/pterodactyl/volumes/"
api_url = ""
api_key = ""

while True:
    try:
        search_and_clean_jars(base_path, webhook_url, api_url, api_key)
        monitor_ssh_failures() 

        ram_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=1)

        if ram_usage > RAM_THRESHOLD and cpu_usage > CPU_THRESHOLD:
            top_proc = get_top_process()
            if top_proc:
                kill_process(top_proc)
        if monitor_bandwidth():
            close_all_ports()
            time.sleep(30)  
            open_all_ports()
    except Exception as e:
        print(f"Erreur dans la boucle principale : {e}")
        pass

