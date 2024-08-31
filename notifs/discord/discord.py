from discord_webhook import DiscordEmbed , DiscordWebhook


def send_to_discord(message):
    import socket
    import os
    from config import discord_notifications , discord_webhook_url
    if discord_notifications:
        webhook = DiscordWebhook(url=discord_webhook_url,username=socket.gethostname() + "(" + os.system('ipconfig') + ")")
        embed = DiscordEmbed(title="Notification", description=message, color=0xff0000)
        webhook.add_embed(embed)
        webhook.execute()
