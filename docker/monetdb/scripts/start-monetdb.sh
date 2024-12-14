#!/bin/bash

################################################################################
# start-monetdb.sh
# 
# Script de démarrage et configuration de MonetDB dans le conteneur Docker
#
# Ce script :
# 1. Initialise un nouveau dbfarm MonetDB
# 2. Configure les permissions et paramètres
# 3. Démarre le daemon MonetDB
# 4. Crée et configure la base de données
#
# Usage:
#   Ce script est appelé automatiquement comme CMD dans le Dockerfile MonetDB
#
# Variables d'environnement:
#   MONETDB_DB      : Nom de la base de données (défaut: databaseannalizationproject)
#   MONETDB_USER    : Nom d'utilisateur (défaut: monetdb)
#   MONETDB_PASSWORD: Mot de passe (défaut: monetdb)
#
# Processus:
#   1. Nettoyage du dbfarm existant
#   2. Création et configuration du nouveau dbfarm
#   3. Démarrage du daemon
#   4. Création de la base de données
#   5. Configuration de l'utilisateur
#
# Notes:
#   - Les temps d'attente (sleep) sont nécessaires pour la stabilité
#   - Le script garde le conteneur en vie avec tail -f
#
# Codes de retour:
#   0: Succès
#   1: Erreur de configuration
#   2: Erreur de démarrage du daemon
#
# Auteurs: 
#   - Grégoire BODIN
#   - Léo BERNARD-BORDIER
################################################################################

echo "🔄 Démarrage de MonetDB..."

# Nettoyage complet du dbfarm existant
echo "🧹 Nettoyage complet du dbfarm..."
rm -rf /var/monetdb5/dbfarm/*

# Initialisation du dbfarm avec les bonnes permissions
echo "📁 Initialisation du dbfarm..."
monetdbd create /var/monetdb5/dbfarm
chown -R monetdb:monetdb /var/monetdb5/dbfarm
chmod -R 750 /var/monetdb5/dbfarm

monetdbd set listenaddr=0.0.0.0 /var/monetdb5/dbfarm
monetdbd set port=50000 /var/monetdb5/dbfarm
monetdbd set control=yes /var/monetdb5/dbfarm

# Démarrage du daemon
echo "🚀 Démarrage du daemon MonetDB..."
monetdbd start /var/monetdb5/dbfarm

# Attente plus longue pour s'assurer que le daemon est prêt
sleep 15

# Vérification et utilisation des variables d'environnement avec valeurs par défaut
DB_NAME=${MONETDB_DB:-databaseannalizationproject}
DB_USER=${MONETDB_USER:-monetdb}
DB_PASSWORD=${MONETDB_PASSWORD:-monetdb}

# Création et configuration de la base de données
echo "💾 Création de la base de données ${DB_NAME}..."
monetdb create "${DB_NAME}"
monetdb release "${DB_NAME}"

# Attente supplémentaire pour la création de la base
sleep 10

# Configuration de l'utilisateur monetdb
echo "👤 Configuration de l'utilisateur monetdb..."
mclient -u monetdb -d "${DB_NAME}" --set "user=${DB_USER}" --set "password=${DB_PASSWORD}" -s "
CREATE USER \"${DB_USER}\" WITH PASSWORD '${DB_PASSWORD}' NAME 'MonetDB Administrator' SCHEMA \"sys\";
GRANT SYSADMIN TO \"${DB_USER}\";
"

echo "✅ MonetDB est prêt !"

# Garder le conteneur en vie et afficher les logs
tail -f /var/monetdb5/dbfarm/merovingian.log
