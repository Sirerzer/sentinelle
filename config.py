# Redémarrer le service Sentinelle après avoir apporté des modifications
# Commande : systemctl restart sentinelle

# AVERTISSEMENT : Si vous n'êtes pas sûr de ce que vous faites, ne modifiez pas ces paramètres !

# ======================
# PARAMÈTRES DE RESSOURCES
# ======================

# Seuil d'utilisation de la RAM pour notifications ou actions (en pourcentage)
RAM_THRESHOLD = 99  

# Seuil d'utilisation du CPU pour notifications ou actions (en pourcentage)
CPU_THRESHOLD = 99 

# Activer ou désactiver la surveillance des seuils d'utilisation des ressources
threshold_monitoring = True

# Seuil de bande passante pour la surveillance (en octets par seconde) (1 Gbit/s = 1 000 000 000 octets/s)
bandwidth_threshold = 1_000_000_000  # 1 Gbit/s

# Interface réseau à surveiller pour la bande passante
network_interface = "eth0"

# Activer ou désactiver la fermeture du port si le seuil de bande passante est dépassé
close_port_on_threshold_exceed = True

# Activer ou désactiver la surveillance de l'utilisation des ressources sur le serveur
usage_monitoring = True

# Activer ou désactiver l'action de tuer les processus si l'utilisation dépasse les seuils
usage_monitoring_kill = True

# ============================
# PARAMÈTRES DES CONTENEURS DOCKER
# ============================

# Activer ou désactiver la surveillance et l'arrêt des conteneurs Docker
docker_check = True

# Activer ou désactiver l'arrêt automatique des conteneurs Docker qui dépassent les seuils
docker_kill = True

# Seuil d'arrêt pour Docker : Ratio de consommation de la RAM (1/3 signifie 33% de la RAM totale)
docker_ram_ratio = '1/3'

# Seuil d'arrêt pour Docker : Ratio de consommation de CPU (1/3 signifie 33% du CPU total)
docker_cpu_ratio = '1/3'

# ============================
# PARAMÈTRES MINECRAFT
# ============================

# Liste des indicateurs pour détecter une activité suspecte dans les serveurs Minecraft
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

# Activer ou désactiver la suspension automatique des serveurs avec des fichiers suspects via Pterodactyl
pterodactyl_suspension = True

# URL de votre panneau Pterodactyl. Laisser vide si l'option Pterodactyl est désactivée.
pterodactyl_api_url = ""

# Clé d'admin pour accéder à votre panneau Pterodactyl. Laisser vide si l'option Pterodactyl est désactivée.
pterodactyl_api_key = ""

# Répertoire où les volumes des serveurs Pterodactyl sont stockés
pterodactyl_base_path = "/var/lib/pterodactyl/volumes/"

# Activer ou désactiver la suppression automatique des fichiers JAR suspects sur les serveurs Minecraft
delete_suspect_jar = True

# ====================
# PARAMÈTRES DE SURVEILLANCE SSH
# ====================

# Activer ou désactiver la surveillance SSH
ssh_monitoring = True

# Nombre maximal de tentatives de connexion SSH échouées avant de prendre des mesures
max_ssh_attempts = 5

# Durée (en minutes) pour bannir une adresse IP après avoir dépassé le nombre maximal de tentatives échouées
ssh_ban_duration = 60  # en minutes

# ========================
# PARAMÈTRES DE NOTIFICATIONS
# ========================

# Activer ou désactiver les notifications sur Discord
discord_notifications = True

# URL du webhook Discord pour les notifications. Laisser vide si les notifications sont désactivées.
discord_webhook_url = ""

# ========================
# MODES DE FONCTIONNEMENT
# ========================

# Modes de fonctionnement :
# - normal : 1 Sentinelle en cours d'exécution
# - turbo : 3 Sentinelle en cours d'exécution
# - turbo+ : 5 Sentinelle en cours d'exécution
# - custom : configuration personnalisée
mode = "normal"

# Configuration des modes personnalisés (laisser vide si non personnalisé)
custom_mode_config = "1"

