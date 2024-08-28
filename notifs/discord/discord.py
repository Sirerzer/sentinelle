from discord_webhook import DiscordEmbed , DiscordWebhook



def send_to_discord(message):
    
    from ...config import webhook_url , Notif_discord
    if Notif_discord:
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(title="Notification", description=message, color=0xff0000)
        webhook.add_embed(embed)
        webhook.execute()
