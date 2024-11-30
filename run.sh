#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonction pour démarrer un service selon l'OS
start_service() {
    local service_name=$1
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start $service_name
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v systemctl &> /dev/null; then
            sudo systemctl start $service_name
        elif command -v service &> /dev/null; then
            sudo service $service_name start
        else
            echo -e "${RED}❌ Impossible de démarrer le service : aucun gestionnaire de service trouvé${NC}"
            return 1
        fi
    fi
}

# Fonction pour configurer le PATH PostgreSQL
setup_postgres_path() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Ajouter PostgreSQL au PATH pour macOS
        if [ -d "/opt/homebrew/opt/postgresql@15/bin" ]; then
            export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
        elif [ -d "/usr/local/opt/postgresql@15/bin" ]; then
            export PATH="/usr/local/opt/postgresql@15/bin:$PATH"
        fi
    fi
}

# Fonction pour vérifier PostgreSQL
check_postgresql() {
    setup_postgres_path
    
    # Vérifier spécifiquement PostgreSQL 15 sur macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! brew list postgresql@15 &>/dev/null; then
            echo -e "${RED}❌ PostgreSQL 15 n'est pas installé via Homebrew${NC}"
            return 1
        fi
        
        # Vérifier si le service est en cours d'exécution
        if ! brew services list | grep postgresql@15 | grep started &>/dev/null; then
            echo -e "${YELLOW}⚠️  PostgreSQL 15 est installé mais n'est pas démarré${NC}"
            echo -e "${BLUE}Démarrage du service...${NC}"
            brew services start postgresql@15
        fi
    fi
    
    if ! command -v psql &> /dev/null; then
        return 1
    fi
    return 0
}

# Fonction pour installer PostgreSQL selon l'OS
install_postgresql() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}❌ Homebrew n'est pas installé${NC}"
            echo -e "${BLUE}Installation de Homebrew...${NC}"
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            if [ $? -ne 0 ]; then
                echo -e "${RED}❌ Erreur lors de l'installation de Homebrew${NC}"
                return 1
            fi
        fi
        echo -e "${BLUE}Installation de PostgreSQL 15 via Homebrew...${NC}"
        brew install postgresql@15
        start_service postgresql@15
        setup_postgres_path
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo -e "${BLUE}Installation de PostgreSQL via apt...${NC}"
            sudo apt-get update
            sudo apt-get install -y postgresql-15
            start_service postgresql
        elif command -v dnf &> /dev/null; then
            echo -e "${BLUE}Installation de PostgreSQL via dnf...${NC}"
            sudo dnf install -y postgresql-server
            sudo postgresql-setup --initdb
            start_service postgresql
        else
            echo -e "${RED}❌ Impossible de déterminer le gestionnaire de paquets${NC}"
            return 1
        fi
    fi
}

# Fonction pour installer MonetDB selon l'OS
install_monetdb() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}Installation de MonetDB via Homebrew...${NC}"
        brew install monetdb
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo -e "${BLUE}Installation de MonetDB via apt...${NC}"
            sudo apt-get update
            sudo apt-get install -y monetdb5-server monetdb5-client
        elif command -v dnf &> /dev/null; then
            echo -e "${RED}❌ Installation manuelle requise pour MonetDB sur RHEL/CentOS${NC}"
            echo -e "${BLUE}Veuillez suivre les instructions sur https://www.monetdb.org/downloads/${NC}"
            return 1
        fi
    fi
}

# Enregistrer le temps de début
start_time=$(date +%s)

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Vérification des prérequis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo -e "${BLUE}📝 Création du fichier .env...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Fichier .env créé à partir de .env.example${NC}"
    else
        # Créer le fichier .env avec les valeurs par défaut
        cat > .env << EOL
# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=databaseannalizationproject
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

# MonetDB Configuration
MONETDB_USER=monetdb
MONETDB_PASSWORD=monetdb
MONETDB_DB=databaseannalizationproject
MONETDB_HOST=127.0.0.1
MONETDB_PORT=50000

# Application Configuration
BATCH_SIZE=1000
DATA_DIR=./data
EOL
        echo -e "${GREEN}✓ Fichier .env créé avec les valeurs par défaut${NC}"
    fi
    
    echo -e "${BLUE}ℹ️  Veuillez vérifier et ajuster les paramètres dans le fichier .env si nécessaire${NC}"
    read -p "Voulez-vous modifier le fichier .env maintenant ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo -e "${RED}⚠️  Aucun éditeur (nano/vim) n'est installé. Veuillez modifier le fichier .env manuellement.${NC}"
        fi
    fi
else
    echo -e "${GREEN}✓ Fichier .env existant${NC}"
fi

# Vérifier PostgreSQL
if ! check_postgresql; then
    echo -e "${RED}❌ PostgreSQL n'est pas installé ou n'est pas dans le PATH${NC}"
    read -p "Voulez-vous installer PostgreSQL ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        install_postgresql
        if ! check_postgresql; then
            echo -e "${RED}❌ Erreur lors de l'installation de PostgreSQL ou de sa configuration${NC}"
            echo -e "${BLUE}💡 Essayez de redémarrer votre terminal et relancer le script${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ PostgreSQL installé avec succès${NC}"
    else
        echo -e "${RED}❌ PostgreSQL est requis pour exécuter ce programme${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ PostgreSQL est installé${NC}"
fi

# Vérifier MonetDB
if ! command -v monetdb &> /dev/null; then
    echo -e "${RED}❌ MonetDB n'est pas installé${NC}"
    read -p "Voulez-vous installer MonetDB ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        install_monetdb
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Erreur lors de l'installation de MonetDB${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ MonetDB installé avec succès${NC}"
    else
        echo -e "${RED}❌ MonetDB est requis pour exécuter ce programme${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ MonetDB est installé${NC}"
fi

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Initialisation du projet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"


# Rendre les scripts exécutables
chmod +x setup_databases.sh
chmod +x run_analysis.sh

# Étape 1 : Configuration des bases de données
echo -e "${BLUE}🔄 Étape 1/2 : Configuration des bases de données...${NC}"
./setup_databases.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de la configuration des bases de données${NC}"
    exit 1
fi

# Étape 2 : Analyse des performances
echo -e "${BLUE}🔄 Étape 2/2 : Lancement de l'analyse...${NC}"
./run_analysis.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'analyse${NC}"
    exit 1
fi

# Calculer le temps d'exécution
end_time=$(date +%s)
execution_time=$((end_time - start_time))

# Convertir en heures, minutes et secondes
hours=$((execution_time / 3600))
minutes=$(( (execution_time % 3600) / 60 ))
seconds=$((execution_time % 60))

echo -e "${GREEN}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            Récapitulatif
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Temps d'exécution total :${NC}"

if [ $hours -gt 0 ]; then
    echo -e "   ${BLUE}$hours heures, $minutes minutes et $seconds secondes${NC}"
elif [ $minutes -gt 0 ]; then
    echo -e "   ${BLUE}$minutes minutes et $seconds secondes${NC}"
else
    echo -e "   ${BLUE}$seconds secondes${NC}"
fi

echo -e "${GREEN}
📊 Les graphiques ont été générés dans le dossier 'results'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" 