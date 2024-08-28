# Sentinelle - Surveillance et Nettoyage Automatique

Sentinelle est une application de surveillance qui détecte les fichiers suspects sur les serveurs et effectue des actions automatiques pour protéger le système. Ce script s'exécute au démarrage et peut suspendre des serveurs, déplacer des fichiers ou envoyer des notifications via un webhook Discord.

## Fonctionnalités

Le script Python `main.py` fournit plusieurs fonctionnalités clés :

1. **Détection des fichiers JAR Minecraft** :
   - **Fonction** : `is_minecraft_server_jar(jar_path)`
   - **Description** : Vérifie si un fichier JAR correspond à un serveur Minecraft en cherchant des indicateurs spécifiques dans le fichier JAR.

2. **Envoi de notifications via Discord** :
   - **Fonction** : `send_to_discord(message, webhook_url)`
   - **Description** : Envoie un message et/ou un fichier à un canal Discord via un webhook pour notifier les événements importants.

3. **Détection de fichiers en cours de téléchargement** :
   - **Fonction** : `is_file_being_uploaded(file_path, wait_time=1)`
   - **Description** : Détecte si un fichier est encore en cours de téléchargement en comparant sa taille à deux moments différents.

4. **Déplacement des fichiers volumineux** :
   - **Fonction** : `move_large_file(file_path, destination_folder)`
   - **Description** : Déplace un fichier vers un nouveau répertoire s'il dépasse une taille spécifique.

5. **Récupération de l'ID du serveur depuis UUID** :
   - **Fonction** : `get_server_id_from_uuid(uuid, api_url, api_key)`
   - **Description** : Récupère l'ID d'un serveur à partir de son UUID en effectuant une requête sur une API.

6. **Suspension d'un serveur via API** :
   - **Fonction** : `suspend_pterodactyl_server(server_id, api_url, api_key)`
   - **Description** : Suspends un serveur à partir de son ID en utilisant une requête API.

7. **Recherche et nettoyage des fichiers JAR** :
   - **Fonction** : `search_and_clean_jars(base_path, webhook_url, api_url, api_key)`
   - **Description** : Parcourt les fichiers JAR dans un répertoire spécifié, nettoie les fichiers non-Minecraft et prend des actions basées sur leur taille et contenu.

## Prérequis

- **Système d'exploitation** : Linux (avec `systemd` installé)
- **Python 3** : Assurez-vous que Python 3 est installé sur le système (`/usr/bin/python3`).
- **Dépendances Python** : `psutil`, `requests`, `discord-webhook`. Ces paquets doivent être installés pour l'environnement Python utilisé par le script.

Pour installer les dépendances Python, exécutez :

```bash
pip install psutil requests discord-webhook
```

## Installation

Suivez les étapes ci-dessous pour installer Sentinelle sur votre serveur.

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

Lors de l'exécution du script, vous serez invité à entrer les informations suivantes :

- **URL du webhook Discord** : URL où les notifications seront envoyées.
- **URL de l'API** : L'URL de l'API pour suspendre les serveurs si nécessaire.
- **Clé API** : Clé API nécessaire pour authentifier les requêtes API.

### Étape 3 : Vérifier le service

Le script configure automatiquement un service `systemd` nommé `sentinelle` pour démarrer au démarrage du système. Pour vérifier l'état du service :

```bash
sudo systemctl status sentinelle.service
```

### Utilisation et Surveillance

- Le service surveille automatiquement les fichiers et prend les actions définies dans le script Python.
- Les logs du service peuvent être consultés via :

    ```bash
    journalctl -u sentinelle.service
    ```

## Dépannage

- **Le service ne démarre pas ?** Vérifiez les logs avec `journalctl -u sentinelle.service`.
- **Problème de permissions ?** Assurez-vous que le script est exécuté avec les privilèges `root`.
- **Dépendances manquantes ?** Installez les dépendances Python manquantes avec `pip`.

## Désinstallation

Pour désinstaller Sentinelle, désactivez et supprimez le service :

```bash
sudo systemctl stop sentinelle.service
sudo systemctl disable sentinelle.service
sudo rm /etc/systemd/system/sentinelle.service
sudo systemctl daemon-reload
sudo rm -rf /etc/sentinelle
```

## Contribution

Les contributions sont les bienvenues. Pour signaler des bugs ou proposer des fonctionnalités, ouvrez une issue sur GitHub.



