# Redémarrer le service Sentinelle après avoir apporté des modifications
# Commande : systemctl restart sentinelle

# AVERTISSEMENT : Si vous n'êtes pas sûr de ce que vous faites, ne modifiez pas ces paramètres !

# Seuil d'utilisation de la RAM pour notifications ou actions (en pourcentage)
RAM_THRESHOLD = 99  

# Seuil d'utilisation du CPU pour notifications ou actions (en pourcentage)
CPU_THRESHOLD = 99 

# Liste des indicateurs Minecraft pour détecter une activité suspecte
minecraft_indicators = [
    'net/minecraft/server/',
    'org/bukkit/',
    'com/destroystokyo/paper/',
    'com/velocitypowered/api/',
    'io/papermc/paper/',
    'META-INF/maven/org.spigotmc/spigot-api/',
    'net/md_5/bungee/',
    'io/papermc/paperclip',
    'org/bukkit/craftbukkit',
    'net/minecraftforge',
]

# Modes de fonctionnement :
# - normal : 1 Sentinelle en cours d'exécution
# - turbo : 3 Sentinelle en cours d'exécution
# - turbo+ : 5 Sentinelle en cours d'exécution
# - custom : configuration personnalisée
modes = "normal"

# Configuration des modes personnalisés (laisser vide si non personnalisé)
modes_config = "1"

# Activer ou désactiver les notifications sur Discord
Notif_discord = True

# URL du webhook Discord pour les notifications. Laisser vide si les notifications sont désactivées.
webhook_url = ""

# Activer ou désactiver la suspension automatique des serveurs avec des fichiers suspects
pterodactyl = True

# URL de votre panneau Pterodactyl. Laisser vide si l'option Pterodactyl est désactivée.
api_url = ""

# Clé d'admin pour accéder à votre panneau Pterodactyl. Laisser vide si l'option Pterodactyl est désactivée.
api_key = ""

# AVERTISSEMENT : Si vous n'êtes pas sûr de ce que vous faites, ne modifiez pas ce chemin !
# Répertoire où les volumes des serveurs Pterodactyl sont stockés
base_path = "/var/lib/pterodactyl/volumes/"

# Activer ou désactiver la suppression automatique des fichiers JAR suspects sur les serveurs Minecraft
delete_suspect_jar_pterodactyl_server = True

# Activer ou désactiver la surveillance SSH
ssh = True

# Nombre maximal de tentatives de connexion SSH échouées avant de prendre des mesures
max_ssh_attempts = 5

# Durée (en minutes) pour bannir une adresse IP après avoir dépassé le nombre maximal de tentatives échouées
ssh_ban_duration = 60  # Durée en minutes

# Activer ou désactiver la surveillance des seuils d'utilisation des ressources
threshold_monitoring = True

# Seuil de bande passante pour la surveillance (en octets par seconde) (1 Gbit/s = 1 000 000 000 octets/s)
threshold = 100000000  # 1 Gbit/s

# Interface réseau à surveiller
interface = "eth0"

# Activer ou désactiver la fermeture du port si le seuil de bande passante est dépassé
close_port = True

# Activer ou désactiver la surveillance de l'utilisation des ressources sur le serveur
usage_monitoring = True

# Activer ou désactiver l'action de tuer les processus si l'utilisation dépasse les seuils
usage_monitoring_kill = True
