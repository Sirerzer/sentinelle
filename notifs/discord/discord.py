from discord_webhook import DiscordEmbed, DiscordWebhook
import subprocess

def send_to_discord(message):
    import socket
    import os
    from config import discord_notifications, discord_webhook_url
    if discord_notifications:
        try:
            ip = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
        except Exception as e:
            ip = 'Unknown IP'

        webhook = DiscordWebhook(url=discord_webhook_url, username=socket.gethostname() + " (" + ip + ")")
        embed = DiscordEmbed(title="Notification", description=message, color=0xff0000)
        webhook.add_embed(embed)
        webhook.execute()