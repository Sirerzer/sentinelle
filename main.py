import time
import threading
from runner.monitor_network import monitor_network
from runner.monitor_resources import monitor_resources
from runner.monitor_files import monitor_files
from runner.monitor_ssh import monitor_ssh
from config import mode, custom_mode_config

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

while True:
    try:
        time.sleep(0.001)  
    except KeyboardInterrupt:
        print("Arrêt du programme...")
        break