from config import RAM_THRESHOLD , CPU_THRESHOLD
import psutil
from monitoring.usage import kill_process , get_top_process 
import time

def monitor_resources():
    while True:
        try:
            ram_usage = psutil.virtual_memory().percent
            cpu_usage = psutil.cpu_percent(interval=1)

            if ram_usage > RAM_THRESHOLD or cpu_usage > CPU_THRESHOLD:
                top_proc = get_top_process()
                if top_proc:
                    kill_process(top_proc)
            time.sleep(15)

        except Exception as e:
            print(f"Erreur dans la surveillance des ressources : {e}")
