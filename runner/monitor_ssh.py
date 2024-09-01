from monitoring.ssh.ssh import monitor_ssh_failures 
import time

def monitor_ssh():
    while True:
        try:
            monitor_ssh_failures()
        except Exception as e:
            print(f"Erreur dans la surveillance des échecs de connexion SSH : {e}")
        time.sleep(30)
