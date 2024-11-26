#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction pour vérifier les erreurs
check_error() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erreur: $1${NC}"
        exit 1
    fi
}

# Fonction pour démarrer PostgreSQL selon l'OS
start_postgresql() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start postgresql@15
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v systemctl &> /dev/null; then
            sudo systemctl start postgresql
        else
            sudo service postgresql start
        fi
    else
        echo -e "${RED}❌ Système d'exploitation non supporté${NC}"
        exit 1
    fi
}

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo -e "${RED}❌ Erreur: Fichier .env manquant. Copiez .env.example vers .env et configurez-le.${NC}"
    exit 1
fi

# Charger les variables depuis le fichier .env
source .env

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
             Initialisation des Bases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Configuration PostgreSQL
echo -e "${BLUE}
🐘 Configuration PostgreSQL
   ├─ Vérification du service...${NC}"

# Vérifier que PostgreSQL est en cours d'exécution
pg_isready -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${BLUE}   ├─ Service arrêté, démarrage...${NC}"
    start_postgresql
    sleep 5
fi

echo -e "${BLUE}   ├─ Création de la base...${NC}"
# Créer la base PostgreSQL
PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} postgres << EOF
DROP DATABASE IF EXISTS "${POSTGRES_DB}";
CREATE DATABASE "${POSTGRES_DB}" WITH OWNER = ${POSTGRES_USER};
GRANT ALL PRIVILEGES ON DATABASE "${POSTGRES_DB}" TO ${POSTGRES_USER};
EOF
check_error "Impossible de créer la base PostgreSQL"

echo -e "${BLUE}   └─ Vérification de l'accès...${NC}"
if PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -d "${POSTGRES_DB}" -c '\q' > /dev/null 2>&1; then
    echo -e "${GREEN}      ✅ Base PostgreSQL '${POSTGRES_DB}' créée et accessible${NC}"
else
    echo -e "${RED}      ❌ Base PostgreSQL '${POSTGRES_DB}' non accessible${NC}"
    exit 1
fi

# 2. Configuration MonetDB
echo -e "${BLUE}
📊 Configuration MonetDB
   ├─ Initialisation du serveur...${NC}"

# Arrêter et nettoyer MonetDB
monetdbd stop ./data/monetdb 2>/dev/null || true
rm -rf ./data/monetdb/*
sleep 2

# Créer le répertoire de données
mkdir -p ./data/monetdb

# Initialiser MonetDB
monetdbd create ./data/monetdb
monetdbd set port=${MONETDB_PORT} ./data/monetdb
monetdbd set control=yes ./data/monetdb
monetdbd set listenaddr=0.0.0.0 ./data/monetdb
monetdbd start ./data/monetdb
check_error "Impossible de démarrer le serveur MonetDB"

echo -e "${BLUE}   ├─ Création de la base...${NC}"
# Créer la base avec mot de passe explicite
monetdb create -p "${MONETDB_PASSWORD}" "${MONETDB_DB}"
monetdb release "${MONETDB_DB}"
monetdb start "${MONETDB_DB}"
check_error "Impossible de créer la base MonetDB"

# Créer le fichier .monetdb pour l'authentification
echo "user=${MONETDB_USER}
password=${MONETDB_PASSWORD}" > ~/.monetdb
chmod 600 ~/.monetdb

echo -e "${BLUE}   └─ Vérification de l'accès...${NC}"
if mclient -h ${MONETDB_HOST} -p ${MONETDB_PORT} -d "${MONETDB_DB}" -s "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}      ✅ Base MonetDB '${MONETDB_DB}' créée et accessible${NC}"
else
    echo -e "${RED}      ❌ Base MonetDB '${MONETDB_DB}' non accessible${NC}"
    echo -e "${BLUE}      Logs MonetDB :${NC}"
    tail -n 20 ./data/monetdb/merovingian.log
    exit 1
fi

# Message de succès final
echo -e "${GREEN}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              ✅ Installation Réussie !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Informations de connexion :

🐘 PostgreSQL :
   ├─ Base    : ${POSTGRES_DB}
   ├─ Hôte    : ${POSTGRES_HOST}
   ├─ Port    : ${POSTGRES_PORT}
   └─ Commande: psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

📊 MonetDB :
   ├─ Base    : ${MONETDB_DB}
   ├─ Hôte    : ${MONETDB_HOST}
   ├─ Port    : ${MONETDB_PORT}
   └─ Commande: mclient -h ${MONETDB_HOST} -p ${MONETDB_PORT} -u ${MONETDB_USER} -d ${MONETDB_DB}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"