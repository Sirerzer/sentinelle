import os
import shutil
import subprocess
import threading
import time
import requests
from runner.monitor_network import monitor_network
from runner.monitor_resources import monitor_resources
from runner.monitor_files import monitor_files
from runner.monitor_ssh import monitor_ssh
from config import mode, custom_mode_config, auto_update


def create_threads():
    resource_thread = threading.Thread(target=monitor_resources, daemon=True)
    network_thread = threading.Thread(target=monitor_network, daemon=True)
    files_thread = threading.Thread(target=monitor_files, daemon=True)
    ssh_thread = threading.Thread(target=monitor_ssh, daemon=True)
    return resource_thread, network_thread, files_thread, ssh_thread


def start_threads(mode):
    mode_counts = {'normal': 1, 'turbo': 3, 'turbo+': 5}
    count = mode_counts.get(mode, 0)

    if mode == 'custom':
        try:
            count = int(custom_mode_config)
        except ValueError:
            print("La configuration des modes personnalisés n'est pas valide.")
            return

    if count > 0:
        for _ in range(count):
            resource_thread, network_thread, files_thread, ssh_thread = create_threads()
            resource_thread.start()
            network_thread.start()
            files_thread.start()
            ssh_thread.start()
            time.sleep(15)
    else:
        print(f"Mode inconnu ou configuration invalide : {mode}. Aucun thread n'a été lancé.")


def move_config_file(src, dest):
    if not os.path.exists(src):
        print(f"Source file {src} does not exist. Skipping move operation.")
        return
    try:
        if os.path.exists(dest):
            os.remove(dest)
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except OSError as e:
        print(f"Erreur lors du déplacement de {src} vers {dest} : {e}")


def clean_directory(directory):
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        print(f"Erreur lors du nettoyage du répertoire {directory} : {e}")


try:
    os.makedirs('/var/sentinelle/backupconfig', exist_ok=True)
except OSError as e:
    print(f"Erreur lors de la création des dossiers : {e}")

start_threads(mode)

while True:
    try:
        if auto_update:
            try:
                response = requests.get("https://raw.githubusercontent.com/Sirerzer/sentinelle/main/version.txt", timeout=10)
                response.raise_for_status()

                version_text = response.text.strip()
                if version_text != "1":
                    try:
                        move_config_file("config.py", "/var/sentinelle/backupconfig/config.py")

                        os.chdir('/etc')  
                        
                        clean_directory('/etc/sentinelle')
                        
                        subprocess.run(["git", "clone", "https://github.com/Sirerzer/sentinelle.git", "/etc/sentinelle"], check=True)

                        move_config_file("/var/sentinelle/backupconfig/config.py", "config.py")
                        os.system("systemctl restart sentinelle")
                    except (shutil.Error, subprocess.CalledProcessError, OSError) as e:
                        print(f"Erreur lors de la mise à jour : {e}")
                        move_config_file("/var/sentinelle/backupconfig/config.py", "config.py")
            except requests.RequestException as e:
                print(f"Erreur de requête : {e}")

        time.sleep(600)  
    except KeyboardInterrupt:
        print("Arrêt du programme...")
        break
