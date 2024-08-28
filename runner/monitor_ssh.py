from monitoring.network.ssh.main import monitor_ssh_failures 


def monitor_ssh():
    while True:
        try:
            monitor_ssh_failures()
        except Exception as e:
            print(f"Erreur dans la surveillance des échecs de connexion SSH : {e}")