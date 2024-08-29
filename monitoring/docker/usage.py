import docker
import psutil
from notifs.discord.discord import send_to_discord
from config import docker_check, docker_kill, docker_ram_ratio, docker_cpu_ratio, docker_network_threshold_mbits

def check_and_stop_containers():
    if docker_check:
        client = docker.from_env()

        total_memory = psutil.virtual_memory().total
        total_cpu = psutil.cpu_count() * 100

        memory_threshold = total_memory * docker_ram_ratio
        cpu_threshold = total_cpu * docker_cpu_ratio

        for container in client.containers.list():
            stats = container.stats(stream=False)
            container_memory = stats['memory_stats']['usage']
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage']
            system_cpu_delta = stats['cpu_stats']['system_cpu_usage']
            cpu_usage = (cpu_delta / system_cpu_delta) * total_cpu

            network_stats = stats['networks']
            total_network_bytes = sum(network['rx_bytes'] + network['tx_bytes'] for network in network_stats.values())
            total_network_mbits = (total_network_bytes * 8) / (1024 * 1024)
            
            if (container_memory > memory_threshold or 
                cpu_usage > cpu_threshold or 
                total_network_mbits > docker_network_threshold_mbits):
                send_to_discord(f"Le conteneur {container.name} dépasse les seuils et sera arrêté.")

                if docker_kill:
                    container.stop()
