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
from runner.monitor_docker import monitor_docker

from config import mode, custom_mode_config


def create_threads():
    resource_thread = threading.Thread(target=monitor_resources, daemon=True)
    network_thread = threading.Thread(target=monitor_network, daemon=True)
    files_thread = threading.Thread(target=monitor_files, daemon=True)
    ssh_thread = threading.Thread(target=monitor_ssh, daemon=True)
    docker_thread = threading.Thread(target=monitor_docker, daemon=True)

    return resource_thread, network_thread, files_thread, ssh_thread, docker_thread


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
            resource_thread, network_thread, files_thread, ssh_thread , docker_thread = create_threads()
            resource_thread.start()
            network_thread.start()
            files_thread.start()
            ssh_thread.start()
            docker_thread.start()
            time.sleep(15)
    else:
        print(f"Mode inconnu ou configuration invalide : {mode}. Aucun thread n'a été lancé.")


start_threads(mode)

while True:
    try:
        time.sleep(600)  
    except KeyboardInterrupt:
        print("Arrêt du programme...")
        break
