#!/bin/bash

# Vérifie si le script est exécuté en tant que root
if [ "$(id -u)" -ne 0 ]; then
    echo "Ce script doit être exécuté en tant que root. Utilisez 'sudo' ou connectez-vous en tant que root."
    exit 1
fi

# Définir les variables
SERVICE_NAME="sentinelle"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
INSTALL_DIR="/etc/sentinelle"
REPO_URL="https://github.com/Sirerzer/sentinelle.git"

# Créer le répertoire d'installation
echo "Création du répertoire d'installation..."
mkdir -p "$INSTALL_DIR"

# Cloner le dépôt
echo "Clonage du dépôt depuis $REPO_URL..."
git clone "$REPO_URL" "$INSTALL_DIR"

# Vérifier si le clonage a réussi
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Erreur : le dépôt n'a pas pu être cloné."
    exit 1
fi

# Installer les dépendances (en supposant qu'il y a un fichier requirements.txt)
echo "Installation des dépendances Python..."
pip3 install docker psutil requests discord-webhook --break-system-packages

# Créer le fichier de service systemd
echo "Création du fichier de service systemd..."
cat <<EOF | tee "$SERVICE_FILE"
[Unit]
Description=Sentinelle - Surveillance et Nettoyage Automatique
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/main.py
Restart=always
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=/usr/bin"

[Install]
WantedBy=multi-user.target
EOF


cat <<EOF | tee "/bin/sentinelle"
python3 /etc/sentinelle/config.py
EOF
# Recharger la configuration de systemd et démarrer le service
echo "Installation du service systemd..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME.service"
systemctl start "$SERVICE_NAME.service"

# Afficher le statut du service
systemctl status "$SERVICE_NAME.service"

# Instructions pour la configuration
echo "Installation terminée. Le service Sentinelle est configuré et en cours d'exécution."
echo "Vous pouvez maintenant modifier la configuration du script en éditant le fichier suivant :"
echo "$INSTALL_DIR/config.py"
nano "$INSTALL_DIR/config.py"
