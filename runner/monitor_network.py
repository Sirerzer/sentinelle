from monitoring.network.main import monitor_bandwidth , close_all_ports , open_all_ports
import time

def monitor_network():
    while True:
        try:
            if monitor_bandwidth():
                close_all_ports()
                time.sleep(30)  
                open_all_ports()
        except Exception as e:
            print(f"Erreur dans la surveillance du réseau : {e}")
