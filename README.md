# Sentinelle - Surveillance et Nettoyage Automatique

Sentinelle est un outil de surveillance destiné à détecter et gérer les fichiers suspects sur les serveurs. Il exécute des actions automatiques pour protéger le système, telles que la suspension de serveurs, le déplacement de fichiers et l'envoi de notifications via un webhook Discord.

## Fonctionnalités

Le script Python `main.py` offre les fonctionnalités suivantes :

1. **Détection des fichiers JAR Minecraft** :
   - **Fonction** : `is_minecraft_server_jar()`
   - **Description** : Identifie les fichiers JAR associés à un serveur Minecraft en recherchant des indicateurs spécifiques dans le contenu du fichier.

2. **Envoi de notifications via Discord** :
   - **Fonction** : `send_to_discord()`
   - **Description** : Envoie des messages et/ou des fichiers à un canal Discord via un webhook pour notifier les événements importants.

3. **Détection de fichiers en cours de téléchargement** :
   - **Fonction** : `is_file_being_uploaded()`
   - **Description** : Détecte si un fichier est en cours de téléchargement en comparant sa taille à différents moments.

4. **Déplacement des fichiers volumineux** :
   - **Fonction** : `move_large_file()`
   - **Description** : Déplace un fichier vers un répertoire spécifique si sa taille dépasse un seuil défini.

5. **Récupération de l'ID du serveur depuis UUID** :
   - **Fonction** : `get_server_id_from_uuid()`
   - **Description** : Obtient l'ID d'un serveur à partir de son UUID via une requête API.

6. **Suspension d'un serveur via API** :
   - **Fonction** : `suspend_pterodactyl_server()`
   - **Description** : Suspend un serveur en utilisant son ID via une requête API.

7. **Recherche et nettoyage des fichiers JAR** :
   - **Fonction** : `search_and_clean_jars()`
   - **Description** : Explore les fichiers JAR dans un répertoire spécifié, nettoie les fichiers non-Minecraft, et prend des mesures selon leur taille et contenu.

8. **Surveillance des ressources système** :
   - **Fonction** : `monitor_system_resources()`
   - **Description** : Surveille l'utilisation de la RAM et du CPU. Si l'utilisation dépasse les seuils définis, le processus le plus gourmand en ressources est tué.
   
   **Sous-fonctions** :
   - **Fonction** : `get_top_process()`
     - **Description** : Identifie le processus consommant le plus de RAM ou de CPU.
   
   - **Fonction** : `kill_process(pid)`
     - **Description** : Termine le processus avec l'ID spécifié pour libérer des ressources système.

9. **Surveillance de la bande passante** :
   - **Fonction** : `monitor_bandwidth()`
   - **Description** : Surveille l'utilisation de la bande passante. Si elle dépasse le seuil, tous les ports sont fermés temporairement avant d'être réouverts.

10. **Gestion des ports** :
    - **Fonction** : `close_all_ports()` et `open_all_ports()`
    - **Description** : Ferme tous les ports pour se protéger contre les attaques, puis les rouvre après une période de sécurité.

11. **Surveillance des échecs de connexion SSH** :
    - **Fonction** : `monitor_ssh_failures()`
    - **Description** : Analyse les échecs de connexion SSH et bannit les IPs suspectes après un certain nombre d'échecs.

## Prérequis

- **Système d'exploitation** : Linux avec `systemd` installé.
- **Python 3** : Assurez-vous que Python 3 est installé (`/usr/bin/python3`).
- **Dépendances Python** : `psutil`, `requests`, `discord-webhook`. Installez-les via :

    ```bash
    pip install psutil requests discord-webhook
    ```

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

3. Exécutez le script d'installation avec les privilèges `root` :

    ```bash
    sudo ./install_sentinelle.sh
    ```

### Étape 2 : Fournir les informations requises

Lors de l'exécution du script, vous serez invité à entrer :

- **URL du webhook Discord** : URL pour envoyer les notifications.
- **URL de l'API** : URL de l'API pour suspendre les serveurs.
- **Clé API** : Clé pour authentifier les requêtes API.

### Étape 3 : Vérifier le service

Le script configure un service `systemd` nommé `sentinelle` pour démarrer au démarrage du système. Vérifiez l'état du service avec :

```bash
sudo systemctl status sentinelle.service
```

### Utilisation et Surveillance

- Le service surveille automatiquement les fichiers et exécute les actions définies dans le script.
- Consultez les logs du service avec :

    ```bash
    journalctl -u sentinelle.service
    ```

## Dépannage

- **Le service ne démarre pas ?** Vérifiez les logs avec `journalctl -u sentinelle.service`.
- **Problèmes de permissions ?** Assurez-vous que le script est exécuté avec les privilèges `root`.
- **Dépendances manquantes ?** Installez les dépendances Python nécessaires avec `pip`.

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

Les contributions sont les bienvenues. Pour signaler des bugs ou proposer des fonctionnalités, ouvrez une issue sur [GitHub](https://github.com/Sirerzer/sentinelle/issues).

