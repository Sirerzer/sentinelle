#!/bin/bash

# Vérifie si le script est exécuté en tant que root
if [ "$(id -u)" -ne 0 ]; then
    echo "Ce script doit être exécuté en tant que root. Utilisez 'sudo' ou connectez-vous en tant que root."
    exit 1
fi

# Nom du fichier de service et de l'application
SERVICE_NAME="sentinelle"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
INSTALL_DIR="/etc/sentinelle"
script_url="https://raw.githubusercontent.com/Sirerzer/sentinelle/main/main.py"


mkdir -p "$INSTALL_DIR"

SCRIPT_PATH="$INSTALL_DIR/main.py"
echo "Téléchargement du script depuis $script_url..."
curl -o "$SCRIPT_PATH" "$script_url"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Erreur : le script n'a pas pu être téléchargé."
    exit 1
fi



echo "Création du fichier de service systemd..."
cat <<EOF | tee "$SERVICE_FILE"
[Unit]
Description=Sentinelle - Surveillance et Nettoyage Automatique
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=always
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=/usr/bin"

[Install]
WantedBy=multi-user.target
EOF

echo "Installation du service systemd..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME.service"
systemctl start "$SERVICE_NAME.service"

systemctl status "$SERVICE_NAME.service"

echo "Installation terminée. Le service Sentinelle est a configuré et en cours d'exécution."
nano "$INSTALL_DIR/config.py"
