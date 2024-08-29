import time
import threading
from runner.monitor_network import monitor_network
from runner.monitor_resources import monitor_resources
from runner.monitor_files import monitor_files
from runner.monitor_ssh import monitor_ssh
from config import mode, custom_mode_config , auto_update

def create_threads():
    resource_thread = threading.Thread(target=monitor_resources, daemon=True)
    network_thread = threading.Thread(target=monitor_network, daemon=True)
    files_thread = threading.Thread(target=monitor_files, daemon=True)
    ssh_thread = threading.Thread(target=monitor_ssh, daemon=True)
    return resource_thread, network_thread, files_thread, ssh_thread

def start_threads(mode):
    if mode in ['normal', 'turbo', 'turbo+']:
        if mode == 'normal':
            count = 1
        elif mode == 'turbo':
            count = 3
        elif mode == 'turbo+':
            count = 5

        for _ in range(count):
            resource_thread, network_thread, files_thread, ssh_thread = create_threads()
            resource_thread.start()
            network_thread.start()
            files_thread.start()
            ssh_thread.start()
            time.sleep(15)

    elif mode == 'custom':
        try:
            count = int(custom_mode_config)
            for _ in range(count):
                resource_thread, network_thread, files_thread, ssh_thread = create_threads()
                resource_thread.start()
                network_thread.start()
                files_thread.start()
                ssh_thread.start()
                time.sleep(15)
        except ValueError:
            print("La configuration des modes personnalisés n'est pas valide.")

    else:
        print(f"Mode inconnu : {mode}. Aucun thread n'a été lancé.")

start_threads(mode)
import requests
import os
import shutil
import subprocess
os.mkdir('/var/sentinelle/backupconfig')



while True:
    try:
        if auto_update:
            response = requests.get("https://raw.githubusercontent.com/Sirerzer/sentinelle/main/version.txt")
            if response.status_code == 200: 
                version_text = response.text.strip()  
                if version_text != "1":
                    shutil.move("config.py" , "/var/sentinelle/backupconfig")
                    subprocess.run(["git", "clone", 'https://github.com/Sirerzer/sentinelle.git', '/var/sentinelle/backupconfig'], check=True)
                    shutil.move("/var/sentinelle/backupconfig/config.py" , "config.py")

            else:
                print(f"Erreur de requête : {response.status_code}")
            
        time.sleep(600)  
    except KeyboardInterrupt:
        print("Arrêt du programme...")
        break