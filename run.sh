#!/bin/bash

################################################################################
# run.sh
# 
# Script principal de lancement du projet Database-Analyzer
#
# Ce script :
# 1. Vérifie les prérequis (Docker, .env)
# 2. Initialise l'environnement du projet
# 3. Lance les conteneurs Docker
# 4. Exécute l'analyse des performances
#
# Usage:
#   ./run.sh
#
# Environnement requis:
#   - Docker et Docker Compose installés
#   - Fichier .env configuré (copié depuis .env.example)
#   - Données CSV dans le dossier data/
#
# Sorties:
#   - Logs dans la console
#   - Résultats dans le dossier results/
#
# Codes de retour:
#   0: Succès
#   1: Erreur de configuration
#   2: Erreur d'exécution Docker
#
# Auteurs: 
#   - Grégoire BODIN
#   - Léo BERNARD-BORDIER
################################################################################

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Vérifier le fichier .env
if [ ! -f .env ]; then
    echo -e "${RED}❌ Erreur: Fichier .env manquant. Copiez .env.example vers .env et configurez-le.${NC}"
    exit 1
fi

# Vérifier Docker et Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker est requis${NC}"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose est requis${NC}"
    exit 1
fi

echo -e "${BLUE}🔄 Initialisation du projet...${NC}"
./scripts/init.sh

# Arrêter et nettoyer les conteneurs existants
echo -e "${BLUE}🔄 Nettoyage des conteneurs...${NC}"
docker compose down -v

# Construire et démarrer les conteneurs
echo -e "${BLUE}🚀 Démarrage des services...${NC}"
if ! docker compose up -d --build; then
    echo -e "${RED}❌ Erreur de démarrage${NC}"
    docker compose logs
    exit 1
fi

# Attendre que les services soient prêts
echo -e "${BLUE}⏳ Attente des services...${NC}"
sleep 30

# Lancer l'analyse
echo -e "${BLUE}📊 Lancement de l'analyse...${NC}"
if ! docker compose run --rm analyzer python -m src.main; then
    echo -e "${RED}❌ Erreur d'analyse${NC}"
    docker compose logs
    exit 1
fi

echo -e "${GREEN}✅ Analyse terminée ! Les résultats sont dans le dossier 'results'${NC}"