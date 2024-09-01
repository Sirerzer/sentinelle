import docker
import psutil
from notifs.discord.discord import send_to_discord
from notifs.SMTP.smtp import send_email

from config import docker_check, docker_kill, docker_ram_ratio, docker_cpu_ratio, docker_network_threshold_mbits

def check_and_stop_containers():
    if docker_check:
        client = docker.from_env()
        bytes_to_gigaoctets = 1_073_741_824
        total_memory = psutil.virtual_memory().total
        total_cpu_count = psutil.cpu_count()
        memory_threshold = total_memory * docker_ram_ratio
        cpu_threshold = total_cpu_count * 100 * docker_cpu_ratio

        previous_network_stats = {}

        while True:
            for container in client.containers.list():
                stats = container.stats(stream=False)
                
                container_memory = stats['memory_stats']['usage']
                
                cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage']
                system_cpu_delta = stats['cpu_stats']['system_cpu_usage']
                cpu_usage = (cpu_delta / system_cpu_delta) * total_cpu_count * 100  

                network_stats = stats['networks']
                current_network_bytes = sum(network['rx_bytes'] + network['tx_bytes'] for network in network_stats.values())

                previous_bytes = previous_network_stats.get(container.id, current_network_bytes)
                network_usage_mbits = ((current_network_bytes - previous_bytes) * 8) / (1024 * 1024)

                previous_network_stats[container.id] = current_network_bytes

                if (container_memory > memory_threshold or 
                    cpu_usage > cpu_threshold or 
                    network_usage_mbits > docker_network_threshold_mbits):
                    send_email(f"Le conteneur {container.name} dépasse les seuils et sera arrêté. CPU: `{cpu_usage:.2f}%` RAM: `{container_memory/bytes_to_gigaoctets}` bytes Réseau: `{network_usage_mbits:.2f} Mbits/s`")
                    send_to_discord(f"Le conteneur {container.name} dépasse les seuils et sera arrêté. CPU: `{cpu_usage:.2f}%` RAM: `{container_memory/bytes_to_gigaoctets}` bytes Réseau: `{network_usage_mbits:.2f} Mbits/s`")

                    if docker_kill:
                        container.stop()

