import psutil
from config import usage_monitoring_kill , usage_monitoring 

def get_top_process():
    if usage_monitoring:
        processes = [(proc, proc.memory_percent(), proc.cpu_percent(interval=0.1))
                     for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent'])]
        processes.sort(key=lambda x: (x[1], x[2]), reverse=True)
        if processes:
            top_proc = processes[0][0]
            print(f"Processus sélectionné pour terminaison: {top_proc.name()} (PID: {top_proc.pid})")
            return top_proc
        else:
            print("Aucun processus à terminer trouvé.")
            return None


def kill_process(proc):
    if usage_monitoring_kill:
        try:
            print(f"Termination du processus: {proc.name()} (PID: {proc.pid})")
            proc.terminate()
            proc.wait(timeout=3)
        except psutil.NoSuchProcess:
            print("Processus déjà terminé.")
        except psutil.AccessDenied:
            print("Permission refusée pour terminer le processus.")
        except Exception as e:
            print(f"Erreur lors de la tentative de terminaison du processus : {e}")
