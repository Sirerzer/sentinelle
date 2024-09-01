# Sentinelle - Surveillance et Nettoyage Automatique

**Sentinelle** est un outil de surveillance conçu pour détecter et gérer les fichiers suspects sur les serveurs. Il exécute des actions automatiques pour protéger le système, comme la suspension de serveurs, le déplacement de fichiers douteux et l'envoi de notifications via un webhook Discord.

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


