#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration du PATH pour PostgreSQL sur macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
fi

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

check_postgres_users() {
    echo -e "${BLUE}
 Liste des utilisateurs PostgreSQL :${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Pour macOS avec Homebrew
        psql -U postgres postgres -c "\du" || {
            echo -e "${RED}❌ Erreur de connexion avec postgres${NC}"
            echo -e "${BLUE}💡 Essayez de créer l'utilisateur postgres :${NC}"
            echo "   createuser -s postgres"
            echo -e "${BLUE}💡 Ou connectez-vous avec l'utilisateur système :${NC}"
            echo "   createuser -s $USER"
        }
    else
        # Pour Linux
        sudo -u postgres psql -c "\du" || {
            echo -e "${RED}❌ Erreur de connexion${NC}"
            echo -e "${BLUE}💡 Vérifiez que PostgreSQL est installé et démarré :${NC}"
            echo "   sudo systemctl status postgresql"
        }
    fi
    
    echo -e "${BLUE}
💡 Pour créer votre utilisateur, exécutez :${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   createuser -s nom-utilisateur"
    else
        echo "   sudo -u postgres createuser -s nom-utilisateur"
    fi
}

postgre_config() {
    echo -e "${BLUE}
🐘 Configuration PostgreSQL
├─ Vérification du service...${NC}"

    # Vérifier si PostgreSQL est installé
    if ! command -v psql &> /dev/null; then
        echo -e "${RED}❌ PostgreSQL n'est pas installé${NC}"
        exit 1
    fi

    # Vérifier que PostgreSQL est en cours d'exécution avec plus de détails
    pg_isready -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${BLUE}   ├─ Service arrêté, démarrage...${NC}"
        start_postgresql
        sleep 5
        
        # Revérifier après le démarrage
        pg_isready -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Impossible de démarrer PostgreSQL${NC}"
            echo -e "${BLUE}Diagnostic :${NC}"
            echo -e "├─ Vérification du statut du service..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew services list | grep postgresql
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                systemctl status postgresql || service postgresql status
            fi
            exit 1
        fi
    fi

    echo -e "${BLUE}   ├─ Test de connexion avec l'utilisateur ${POSTGRES_USER}...${NC}"
    if ! PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -c '\conninfo' postgres &>/dev/null; then
        echo -e "${RED}❌ Erreur de connexion. Vérifiez vos paramètres :${NC}"
        echo -e "   ├─ Utilisateur : ${POSTGRES_USER}"
        echo -e "   ├─ Hôte       : ${POSTGRES_HOST}"
        echo -e "   ├─ Port       : ${POSTGRES_PORT}"
        echo -e "   └─ Base       : postgres"
        check_postgres_users
        exit 1
    fi

    echo -e "${BLUE}   ├─ Création de la base...${NC}"
# Créer la base PostgreSQL
    echo -e "${BLUE}      ├─ Suppression de l'ancienne base si elle existe...${NC}"
    psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} postgres -c "DROP DATABASE IF EXISTS \"${POSTGRES_DB}\";" > /dev/null 2>&1
    echo -e "${GREEN}      │  ✓ Nettoyage effectué${NC}"
    echo -e "${BLUE}      ├─ Création de la nouvelle base...${NC}"
    PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} postgres -c "CREATE DATABASE \"${POSTGRES_DB}\" WITH OWNER = ${POSTGRES_USER};" > /dev/null 2>&1
    echo -e "${GREEN}      │  ✓ Base créée${NC}"

    echo -e "${BLUE}      └─ Configuration des permissions...${NC}"
    PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"${POSTGRES_DB}\" TO ${POSTGRES_USER};" > /dev/null 2>&1
    echo -e "${GREEN}         ✓ Permissions accordées${NC}"

    echo -e "${BLUE}   └─ Vérification de l'accès...${NC}"
    if PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -d "${POSTGRES_DB}" -c '\q' > /dev/null 2>&1; then
        echo -e "${GREEN}      ✅ Base PostgreSQL '${POSTGRES_DB}' créée et accessible${NC}"
    else
        echo -e "${RED}      ❌ Base PostgreSQL '${POSTGRES_DB}' non accessible${NC}"
        exit 1
    fi
}

monetdb_config() {
    echo -e "${BLUE}
📊 Configuration MonetDB
├─ Initialisation du serveur...${NC}"

# Arrêter et nettoyer MonetDB
    echo -e "${BLUE}      ├─ Arrêt du serveur existant...${NC}"
    monetdbd stop ./data/monetdb 2>/dev/null || true
    echo -e "${GREEN}      │  ✓ Serveur arrêté${NC}"

    echo -e "${BLUE}      ├─ Nettoyage des anciennes données...${NC}"
    rm -rf ./data/monetdb/*
    echo -e "${GREEN}      │  ✓ Données nettoyées${NC}"

# Créer le répertoire de données
    echo -e "${BLUE}      ├─ Création du répertoire de données...${NC}"
    mkdir -p ./data/monetdb
    echo -e "${GREEN}      │  ✓ Répertoire créé${NC}"

# Initialiser MonetDB
    echo -e "${BLUE}      ├─ Configuration du serveur...${NC}"
    monetdbd create ./data/monetdb > /dev/null 2>&1
    monetdbd set port=${MONETDB_PORT} ./data/monetdb > /dev/null 2>&1
    monetdbd set control=yes ./data/monetdb > /dev/null 2>&1
    monetdbd set listenaddr=0.0.0.0 ./data/monetdb > /dev/null 2>&1
    echo -e "${GREEN}      │  ✓ Configuration effectuée${NC}"

    echo -e "${BLUE}      └─ Démarrage du serveur...${NC}"
    monetdbd start ./data/monetdb > /dev/null 2>&1
    check_error "Impossible de démarrer le serveur MonetDB"
    echo -e "${GREEN}         ✓ Serveur démarré${NC}"

    echo -e "${BLUE}   ├─ Création de la base...${NC}"
# Créer la base avec mot de passe explicite
    echo -e "${BLUE}      ├─ Création de la nouvelle base...${NC}"
    monetdb create -p "${MONETDB_PASSWORD}" "${MONETDB_DB}" > /dev/null 2>&1
    echo -e "${GREEN}      │  ✓ Base créée${NC}"

    echo -e "${BLUE}      ├─ Configuration des permissions...${NC}"
    monetdb release "${MONETDB_DB}" > /dev/null 2>&1
    echo -e "${GREEN}      │  ✓ Base libérée${NC}"

    echo -e "${BLUE}      └─ Démarrage de la base...${NC}"
    monetdb start "${MONETDB_DB}" > /dev/null 2>&1
    check_error "Impossible de démarrer la base MonetDB"
    echo -e "${GREEN}         ✓ Base démarrée${NC}"

# Créer le fichier .monetdb pour l'authentification
    echo -e "${BLUE}   ├─ Configuration de l'authentification...${NC}"
    echo -e "${BLUE}   └─ Vérification de l'accès...${NC}"
    if mclient -h ${MONETDB_HOST} -p ${MONETDB_PORT} -d "${MONETDB_DB}" -s "SELECT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}      ✅ Base MonetDB '${MONETDB_DB}' créée et accessible${NC}"
    else
        echo -e "${RED}      ❌ Base MonetDB '${MONETDB_DB}' non accessible${NC}"
        echo -e "${BLUE}      Logs MonetDB :${NC}"
        tail -n 20 ./data/monetdb/merovingian.log
        exit 1
fi
}

# Fonction pour demander une confirmation à l'utilisateur
select_option() {
    local prompt=$1
    local response

    while true; do
        echo -en "${BLUE}${prompt} (o/n) ${NC}"
        read -r response
        case "$response" in
            [oO]|[oO][uU][iI]) return 0 ;;
            [nN]|[nN][oO][nN]) return 1 ;;
            *) echo -e "${RED}Veuillez répondre par 'o' pour oui ou 'n' pour non.${NC}" ;;
        esac
    done
}

# Modification de la fonction check_existing_databases
check_existing_databases() {
    local postgres_is_created=false
    local monetdb_is_created=false
    
    echo -e "${BLUE}🔍 Vérification des bases existantes...${NC}"
    
    # Vérifier PostgreSQL
    if ! PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -lqt >/dev/null 2>&1; then
        postgre_config
        postgres_is_created=true
    else
        if PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -lqt | cut -d \| -f 1 | grep -qw "${POSTGRES_DB}"; then
            if select_option "├─ Base PostgreSQL '${POSTGRES_DB}' existe déjà. Souhaitez-vous la recréer ?"; then
                postgre_config
                postgres_is_created=true
            else
                echo -e "${BLUE}├─ ℹ Base PostgreSQL conservée${NC}"
            fi
        fi
    fi
    
    # Vérifier MonetDB
    if [ -d "./data/monetdb/${MONETDB_DB}" ]; then
        if select_option "└─ Base MonetDB '${MONETDB_DB}' existe déjà. Souhaitez-vous la recréer ?"; then
            monetdb_config
            monetdb_is_created=true
        else
            echo -e "${BLUE}└─ ℹ Base MonetDB conservée${NC}"
        fi
    fi
    
    if [ "$postgres_is_created" = false ] && [ "$monetdb_is_created" = false ]; then
        echo -e "${BLUE}\nAucune modification effectuée.${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        exit 0
    fi
}

# Appeler la fonction de vérification
check_existing_databases


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

