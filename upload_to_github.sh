#!/bin/bash

# Set variables
REPO_DIR="/Users/markusaltenburger/Documents/MyScripts/Python-Kurs"  # Pfad zum lokalen Repository
COMMIT_MSG="Automatischer Upload vom Mac Mini am $(date)"

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
