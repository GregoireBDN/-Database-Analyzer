#!/bin/bash

################################################################################
# init.sh
# 
# Script d'initialisation du projet Database-Analyzer
#
# Ce script :
# 1. Crée les dossiers nécessaires (data/, results/)
# 2. Configure le fichier .env s'il n'existe pas
# 3. Vérifie la présence des fichiers de données requis
#
# Usage:
#   ./scripts/init.sh
#
# Structure créée:
#   project/
#   ├── data/              # Dossier pour les fichiers CSV
#   │   └── air_quality.csv
#   └── results/           # Dossier pour les graphiques générés
#
# Prérequis:
#   - Fichier .env.example présent à la racine
#   - Droits d'écriture dans le dossier courant
#
# Codes de retour:
#   0: Succès
#   1: Fichiers de données manquants
#   2: Erreur de création des dossiers
#
# Notes:
#   - Le script vérifie la présence du fichier air_quality.csv
#   - Copie automatiquement .env.example vers .env si nécessaire
#
# Auteurs: 
#   - Grégoire BODIN
#   - Léo BERNARD-BORDIER
################################################################################

# Création des dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p data
mkdir -p results

# Création du fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📄 Création du fichier .env..."
    if ! cp .env.example .env; then
        echo "⚠️  Impossible de créer le fichier .env"
        echo "   Vérifiez que .env.example existe et est accessible"
        exit 2
    fi
fi

# Vérification des fichiers de données
if [ ! -f "data/air_quality.csv" ]; then
    echo "⚠️  Le fichier data/air_quality.csv est manquant"
    echo "   Veuillez placer vos fichiers CSV dans le dossier 'data'"
    exit 1
fi 

echo "✅ Initialisation terminée avec succès"
exit 0 