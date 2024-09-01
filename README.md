# Sentinelle - Surveillance et Nettoyage Automatique

**Sentinelle** est un outil de surveillance conçu pour détecter et gérer les fichiers suspects sur les serveurs. Il exécute des actions automatiques pour protéger le système, comme la suspension de serveurs, le déplacement de fichiers douteux et l'envoi de notifications via un webhook Discord.

[![Python package](https://github.com/Sirerzer/sentinelle/actions/workflows/python-app.yml/badge.svg)](https://github.com/Sirerzer/sentinelle/actions/workflows/python-app.yml)

## Fonctionnalités

Sentinelle propose les fonctionnalités suivantes :

1. Détection des fichiers JAR qui ne sont pas des serveurs Minecraft (uniquement pour Pterodactyl).
2. Gestion de la consommation des ressources Docker (via `config.py`).
3. Surveillance des ressources : en cas de consommation excessive, le programme termine automatiquement le processus le plus gourmand.
4. Blocage des adresses IP effectuant des tentatives de force brute sur SSH.
5. Notifications en temps réel via Discord ou SMTP.
6. Suspension des serveurs contenant de faux fichiers JAR ou d'autres anomalies.

## Installation

Suivez ces étapes pour installer Sentinelle sur votre serveur :

### Étape 1 : Télécharger et exécuter le script d'installation

1. Téléchargez le script d'installation :

    ```bash
    wget -O install_sentinelle.sh https://raw.githubusercontent.com/Sirerzer/sentinelle/main/install.sh
    ```

2. Rendez le script exécutable :

    ```bash
    chmod +x install_sentinelle.sh
    ```

3. Exécutez le script d'installation avec les privilèges root :

    ```bash
    sudo ./install_sentinelle.sh
    ```

### Étape 2 : Vérifier le service

Le script configure un service `systemd` nommé `sentinelle` pour démarrer automatiquement au lancement du système. Pour vérifier l'état du service, exécutez :

```bash
sudo systemctl status sentinelle.service
```

###  Étape 3 : Vérifier la configuration
Si rien n'est retourné tout fonction

```bash
sudo sentinelle
```

## Utilisation et Surveillance

- Sentinelle surveille automatiquement les fichiers et exécute les actions définies dans le script.
- Consultez les journaux du service avec la commande suivante :

    ```bash
    journalctl -u sentinelle.service
    ```

## Dépannage

- **Le service ne démarre pas ?** Vérifiez les journaux avec `journalctl -u sentinelle.service`.
- **Problèmes de permissions ?** Assurez-vous que le script est exécuté avec les privilèges root.
- **Dépendances manquantes ?** Installez les dépendances Python nécessaires via `pip`.

## Config

| **Paramètre**                              | **Valeur par défaut**                          | **Description**                                                                                                                                             |
|--------------------------------------------|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `RAM_THRESHOLD`                            | 95                                             | Seuil d'utilisation de la RAM (en %) pour les notifications ou actions.                                                                                     |
| `CPU_THRESHOLD`                            | 95                                             | Seuil d'utilisation du CPU (en %) pour les notifications ou actions.                                                                                         |
| `threshold_monitoring`                     | True                                           | Surveillance de l'utilisation des ressources (True pour activer, False pour désactiver).                                                                     |
| `bandwidth_threshold`                      | 1_000_000_000                                  | Seuil de bande passante pour la surveillance (en octets par seconde, 1 Gbit/s = 1 000 000 000 octets/s).                                                     |
| `network_interface`                        | "eth0"                                         | Interface réseau à surveiller pour la bande passante.                                                                                                        |
| `close_port_on_threshold_exceed`           | False                                           | Fermeture automatique des ports si le seuil de bande passante est dépassé.                                                                                   |
| `usage_monitoring`                         | True                                           | Surveillance de l'utilisation des ressources sur le serveur.                                                                                                |
| `usage_monitoring_kill`                    | True                                           | Action de tuer les processus si l'utilisation dépasse les seuils.                                                                                            |
| `ram_optimisateur`                         | False                                          | Activation de l'optimisation de la RAM.                                                                                                                     |
| `docker_check`                             | True                                           | Surveillance et arrêt des conteneurs Docker (True pour activer, False pour désactiver).                                                                      |
| `docker_kill`                              | True                                           | Arrêt automatique des conteneurs Docker qui dépassent les seuils.                                                                                            |
| `docker_ram_ratio`                         | 1/3                                            | Ratio de consommation de la RAM pour arrêter Docker (1/3 signifie 33%).                                                                                     |
| `docker_cpu_ratio`                         | 1/3                                            | Ratio de consommation du CPU pour arrêter Docker (1/3 signifie 33%).                                                                                        |
| `docker_network_threshold_mbits`           | 100                                            | Seuil de consommation réseau pour Docker (en Mbits).                                                                                                        |
| `minecraft_indicators`                     | Voir liste                                      | Indicateurs pour détecter une activité suspecte dans les serveurs Minecraft.                                                                                 |
| `pterodactyl_suspension`                   | True                                           | Suspension automatique des serveurs Minecraft avec des fichiers suspects via Pterodactyl.                                                                    |
| `pterodactyl_api_url`                      | ""                                             | URL de votre panneau Pterodactyl.                                                                                                                           |
| `pterodactyl_api_key`                      | ""                                             | Clé d'admin pour accéder à votre panneau Pterodactyl.                                                                                                        |
| `pterodactyl_base_path`                    | "/var/lib/pterodactyl/volumes/"                | Répertoire des volumes de serveurs pour Pterodactyl.                                                                                                         |
| `delete_suspect_jar`                       | True                                           | Suppression automatique des fichiers JAR suspects sur les serveurs Minecraft.                                                                                |
| `ssh_monitoring`                           | True                                           | Surveillance SSH (True pour activer, False pour désactiver).                                                                                                |
| `max_ssh_attempts`                         | 5                                              | Nombre maximal de tentatives de connexion SSH échouées avant de prendre des mesures.                                                                         |
| `ssh_ban_duration`                         | 60                                             | Durée de bannissement d'une adresse IP après dépassement du nombre maximal de tentatives échouées (en minutes).                                               |
| `ssh_notifications`                        | False                                          | Notifications SSH (False par défaut).                                                                                                                       |
| `discord_notifications`                    | True                                           | Notifications sur Discord (True pour activer, False pour désactiver).                                                                                       |
| `discord_webhook_url`                      | ""                                             | URL du webhook Discord.                                                                                                                                     |
| `smtp_notifications`                       | False                                          | Activer ou désactiver les notifications par SMTP.                                                                                                            |
| `smtp_server`                              | "smtp.example.com"                             | Serveur SMTP pour les notifications.                                                                                                                        |
| `smtp_port`                                | 465                                            | Port du serveur SMTP.                                                                                                                                       |
| `smtp_username`                            | "votre_adresse_email@example.com"              | Nom d'utilisateur pour le serveur SMTP.                                                                                                                     |
| `smtp_password`                            | "votre_mot_de_passe"                           | Mot de passe pour le serveur SMTP.                                                                                                                          |
| `email_from`                               | "votre_adresse_email@example.com"              | Adresse e-mail de l'expéditeur.                                                                                                                             |
| `email_to`                                 | "destinataire@example.com"                     | Adresse e-mail du destinataire.                                                                                                                             |
| `mode`                                      | "normal"                                       | Modes de fonctionnement : normal (1 Sentinelle), turbo (3 Sentinelle), turbo+ (5 Sentinelle), custom (configuration personnalisée).                          |
| `custom_mode_config`                       | 1                                              | Configuration des modes personnalisés (laisser vide si non utilisé).                                                                                        |

## Désinstallation

Pour désinstaller Sentinelle, arrêtez et supprimez le service :

```bash
sudo systemctl stop sentinelle.service
sudo systemctl disable sentinelle.service
sudo rm /etc/systemd/system/sentinelle.service
sudo systemctl daemon-reload
sudo rm -rf /etc/sentinelle
```

## Contribution

Les contributions sont les bienvenues ! Pour signaler des bugs ou proposer de nouvelles fonctionnalités, ouvrez une issue sur [GitHub](https://github.com/Sirerzer/sentinelle/issues).


