import zipfile 
from config import minecraft_indicators , webhook_url , api_key ,api_url ,base_path
from utils.files import is_file_being_uploaded , move_large_file
import glob
from notifs.discord.discord import send_to_discord
from discord_webhook import DiscordWebhook
import os
from pterodactyl.main import suspend_pterodactyl_server


def is_minecraft_server_jar(jar_path):
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            for file_name in jar.namelist():
                if any(indicator in file_name for indicator in minecraft_indicators):
                    return True
        return False
    except:
        pass

def search_and_clean_jars(base_path=base_path, api_url=api_url, api_key=api_key):
    jar_paths = glob.glob(os.path.join(base_path, '*/*.jar'))
    for jar_path in jar_paths:
        uuid = os.path.basename(os.path.dirname(jar_path))
        if is_file_being_uploaded(jar_path):
            print(f"File is still uploading: {jar_path}")
            continue
        
        if not is_minecraft_server_jar(jar_path):
            print(f"Non-Minecraft JAR detected: {jar_path}")
            file_size_mb = os.path.getsize(jar_path) / (1024 * 1024)
            
            if file_size_mb > 8:  
                new_path = move_large_file(jar_path, f"/var/sentinelle/{uuid}")
                send_to_discord(f"File moved to: {new_path}")
            else:
                send_to_discord(f"Non-Minecraft JAR detected and sent: {jar_path}")
                with open(jar_path, "rb") as f:
                    webhook = DiscordWebhook(url=webhook_url)
                    webhook.add_file(file=f.read(), filename=os.path.basename(jar_path))
                    webhook.execute()
                os.remove(jar_path)
            
          
                if suspend_pterodactyl_server(uuid, api_url, api_key):
                    send_to_discord(f"Server {uuid} suspended due to suspicious JAR file.", webhook_url)
                
