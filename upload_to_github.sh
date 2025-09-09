#!/bin/bash

# Set variables
#REPO_DIR="/Users/markusaltenburger/Documents/MyScripts/Python"  # Pfad zum lokalen Repository
#REPO_DIR="/home/pi/Documents/MyScripts/Python"  # Pfad zum lokalen Repository
REPO_DIR="./"  # Pfad zum lokalen Repository


COMMIT_MSG="Automatischer Upload vom Host $(hostname) am $(date)"

# Wechsle ins Repository-Verzeichnis
cd "$REPO_DIR" || { echo "Repository-Verzeichnis nicht gefunden."; exit 1; }

# Füge alle Änderungen hinzu
git add .

# Commit mit Nachricht
git commit -m "$COMMIT_MSG"

# Push zu GitHub über SSH
if git push origin main; then
    echo "✅ Upload erfolgreich abgeschlossen."
else
    echo "❌ Upload fehlgeschlagen."
fi
