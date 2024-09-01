# ======================
# Instructions et Avertissements
# ======================

# Redémarrer le service Sentinelle après avoir apporté des modifications
# Commande : systemctl restart sentinelle

# AVERTISSEMENT : Ne modifiez pas ces paramètres si vous n'êtes pas certain de ce que vous faites !

# ======================
# PARAMÈTRES DE RESSOURCES
# ======================

# Seuil d'utilisation de la RAM et du CPU pour notifications ou actions (en pourcentage)
RAM_THRESHOLD = 95  # Seuil de la RAM (en %)
CPU_THRESHOLD = 95  # Seuil du CPU (en %)

# Surveillance de l'utilisation des ressources (True pour activer, False pour désactiver)
threshold_monitoring = True

# Seuil de bande passante pour la surveillance (en octets par seconde, 1 Gbit/s = 1 000 000 000 octets/s)
bandwidth_threshold = 1_000_000_000  # 1 Gbit/s

# Interface réseau à surveiller pour la bande passante
network_interface = "eth0"

# Fermeture automatique des ports si le seuil de bande passante est dépassé
close_port_on_threshold_exceed = False

# Surveillance de l'utilisation des ressources sur le serveur
usage_monitoring = True

# Action de tuer les processus si l'utilisation dépasse les seuils
usage_monitoring_kill = True

# Activation de l'optimisation de la RAM (False par défaut)
ram_optimisateur = False

# ============================
# PARAMÈTRES DES CONTENEURS DOCKER
# ============================

# Surveillance et arrêt des conteneurs Docker (True pour activer, False pour désactiver)
docker_check = True

# Arrêt automatique des conteneurs Docker qui dépassent les seuils
docker_kill = True

# Seuils pour Docker : Ratio de consommation de la RAM et du CPU (1/3 signifie 33% de la RAM ou du CPU total)
docker_ram_ratio = 1/3  # Ratio de RAM pour arrêter Docker
docker_cpu_ratio = 1/3  # Ratio de CPU pour arrêter Docker

# Seuil de consommation réseau pour Docker (en Mbits)
docker_network_threshold_mbits = 100

# ============================
# PARAMÈTRES MINECRAFT
# ============================

# Indicateurs pour détecter une activité suspecte dans les serveurs Minecraft
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

# Suspension automatique des serveurs Minecraft avec des fichiers suspects via Pterodactyl
pterodactyl_suspension = True

# Configuration Pterodactyl
pterodactyl_api_url = ""  # URL de votre panneau Pterodactyl
pterodactyl_api_key = ""  # Clé d'admin pour accéder à votre panneau Pterodactyl
pterodactyl_base_path = "/var/lib/pterodactyl/volumes/"  # Répertoire des volumes de serveurs

# Suppression automatique des fichiers JAR suspects sur les serveurs Minecraft
delete_suspect_jar = True

# ====================
# PARAMÈTRES DE SURVEILLANCE SSH
# ====================

# Surveillance SSH (True pour activer, False pour désactiver)
ssh_monitoring = True

# Nombre maximal de tentatives de connexion SSH échouées avant de prendre des mesures
max_ssh_attempts = 5

# Durée de bannissement d'une adresse IP après dépassement du nombre maximal de tentatives échouées (en minutes)
ssh_ban_duration = 60  

# Notifications SSH (False par défaut)
ssh_notifications = False

# ========================
# PARAMÈTRES DE NOTIFICATIONS PAR DISCORD
# ========================

# Notifications sur Discord (True pour activer, False pour désactiver)
discord_notifications = True
discord_webhook_url = ""  # URL du webhook Discord

# ========================
# PARAMÈTRES DE NOTIFICATIONS PAR SMTP
# ========================

# Activer ou désactiver les notifications par SMTP
smtp_notifications = False

# Configuration du serveur SMTP
smtp_server = "smtp.example.com"
smtp_port = 465
smtp_username = "votre_adresse_email@example.com"
smtp_password = "votre_mot_de_passe"

# Adresse e-mail de l'expéditeur et du destinataire
email_from = "votre_adresse_email@example.com"
email_to = "destinataire@example.com"

# ========================
# MODES DE FONCTIONNEMENT
# ========================

# Modes de fonctionnement :
# - normal : 1 Sentinelle en cours d'exécution
# - turbo  : 3 Sentinelle en cours d'exécution
# - turbo+ : 5 Sentinelle en cours d'exécution
# - custom : configuration personnalisée
mode = "normal"

# Configuration des modes personnalisés (laisser vide si non utilisé)
custom_mode_config = 1







