#!/bin/bash

# Désactiver tous les éditeurs interactifs
export EDITOR=cat
export VISUAL=cat
export MONETDB_EDITOR=cat
export MAPI_EDITOR=cat

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
YELLOW='\033[1;33m'



# Charger les variables d'environnement
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}❌ Fichier .env manquant${NC}"
    exit 1
fi

# Vérifier que MONETDB_DB est défini
if [ -z "${MONETDB_DB}" ]; then
    echo -e "${RED}❌ La variable MONETDB_DB n'est pas définie dans le fichier .env${NC}"
    exit 1
fi

check_monetdb_status() {
    echo -e "${BLUE}📊 Vérification du statut de MonetDB...${NC}"

    # Arrêter proprement MonetDB s'il est en cours d'exécution
    if pgrep monetdbd > /dev/null; then
        echo -e "${BLUE}🔄 Arrêt des instances MonetDB existantes...${NC}"
        monetdbd stop ./data/monetdb 2>/dev/null || true
        sleep 2
        pkill -9 -f monetdbd 2>/dev/null || true
        sleep 2
    fi

    # Vérifier si le port 50000 est déjà utilisé
    if lsof -i :50000 > /dev/null; then
        echo -e "${RED}❌ Le port 50000 est déjà utilisé${NC}"
        return 1
    fi

    # 1. Créer le fichier de configuration MonetDB
    mkdir -p ~/.monetdb
    cat > ~/.monetdb/.monetdb << EOF
quiet=yes
editor=cat
EOF

    # 2. Arrêter tous les processus MonetDB existants
    pkill -f monetdbd 2>/dev/null

    # 3. Nettoyer et recréer le répertoire de données
    echo -e "${BLUE}🔄 Réinitialisation de MonetDB...${NC}"
    rm -rf ./data/monetdb
    mkdir -p ./data/monetdb
    
    # 4. Configurer et démarrer MonetDB
    MONETDB_QUIET=yes \
    MONETDB_EDITOR=cat \
    EDITOR=cat \
    VISUAL=cat \
    monetdbd create ./data/monetdb >/dev/null 2>&1
    
    MONETDB_QUIET=yes \
    monetdbd set port=50000 ./data/monetdb >/dev/null 2>&1
    
    echo -e "${BLUE}🚀 Démarrage du serveur MonetDB...${NC}"
    monetdbd start ./data/monetdb >/dev/null 2>&1

    # 5. Créer et configurer la base de données
    echo -e "${BLUE}📦 Création de la base de données ${MONETDB_DB}...${NC}"
    MONETDB_QUIET=yes \
    MONETDB_EDITOR=cat \
    monetdb -q create "${MONETDB_DB}" >/dev/null 2>&1
    
    MONETDB_QUIET=yes \
    MONETDB_EDITOR=cat \
    monetdb -q release "${MONETDB_DB}" >/dev/null 2>&1
    
    # 6. Démarrer la base de données
    echo -e "${BLUE}🔄 Démarrage de la base de données ${MONETDB_DB}...${NC}"
    MONETDB_QUIET=yes \
    MONETDB_EDITOR=cat \
    monetdb -q start "${MONETDB_DB}" >/dev/null 2>&1

    # 7. Vérifier le statut
    if MONETDB_QUIET=yes monetdb -q status | grep "${MONETDB_DB}" | grep -q "R"; then
        echo -e "${GREEN}✓ MonetDB est configuré et démarré${NC}"
        echo -e "${BLUE}📊 Informations de connexion MonetDB :${NC}"
        echo -e "   Base    : ${MONETDB_DB}"
        echo -e "   Port    : ${MONETDB_PORT}"
        return 0
    else
        echo -e "${RED}❌ Impossible de démarrer MonetDB${NC}"
        return 1
    fi
}

# Fonction pour installer Python selon l'OS
install_python() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}Installation de Python via Homebrew...${NC}"
        if ! command -v brew &> /dev/null; then
            echo -e "${BLUE}Installation de Homebrew...${NC}"
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python@3.11
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            echo -e "${BLUE}Installation de Python via apt...${NC}"
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v dnf &> /dev/null; then
            echo -e "${BLUE}Installation de Python via dnf...${NC}"
            sudo dnf install -y python3 python3-pip python3-virtualenv
        else
            echo -e "${RED}❌ Impossible de déterminer le gestionnaire de paquets${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Système d'exploitation non supporté${NC}"
        exit 1
    fi
}

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Configuration de l'environnement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Vérifier si python3 est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    read -p "Voulez-vous installer Python3 ? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        install_python
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Erreur lors de l'installation de Python${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ Python installé avec succès${NC}"
    else
        echo -e "${RED}❌ Python3 est requis pour exécuter ce programme${NC}"
        exit 1
    fi
fi

# Vérifier la version de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${BLUE}Version de Python détectée : ${PYTHON_VERSION}${NC}"

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 n'est pas installé${NC}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}Installation de pip via Homebrew...${NC}"
        brew install pip3
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${BLUE}Installation de pip...${NC}"
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-pip
        fi
    fi
fi

# Créer et activer l'environnement virtuel
echo -e "${BLUE} Création de l'environnement virtuel...${NC}"
python3 -m venv venv

# Activer l'environnement virtuel selon l'OS
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
else
    echo -e "${RED}❌ Système d'exploitation non supporté${NC}"
    exit 1
fi

# Vérifier si l'activation a réussi
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'activation de l'environnement virtuel${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Environnement virtuel activé${NC}"

# Modifier la section de mise à jour de pip
echo -e "${BLUE}📥 Mise à jour de pip...${NC}"


# Tenter la mise à jour avec une meilleure gestion des erreurs
for i in {1..3}; do
    if python3 -m pip install --upgrade pip --timeout 30; then
        echo -e "${GREEN}✓ pip mis à jour avec succès${NC}"
        
        break
    else
        if [ $i -eq 3 ]; then
            echo -e "${YELLOW}⚠️  Impossible de mettre à jour pip. Continuation avec la version actuelle...${NC}"
            
        else
            echo -e "${YELLOW}⚠️  Tentative $i échouée, nouvelle tentative dans 5 secondes...${NC}"
        fi
    fi
done

# Modifier la section d'installation des dépendances
echo -e "${BLUE}📥 Installation des dépendances...${NC}"


# Tenter l'installation avec une meilleure gestion des erreurs
for i in {1..3}; do
    if pip install -r requirements.txt --timeout 30; then
        echo -e "${GREEN}✓ Dépendances installées avec succès${NC}"
        
        break
    else
        if [ $i -eq 3 ]; then
            echo -e "${RED}❌ Erreur lors de l'installation des dépendances après 3 tentatives${NC}"
            echo -e "${BLUE}💡 Suggestions :${NC}"
            echo "   1. Vérifiez votre connexion internet"
            echo "   2. Essayez avec --no-cache-dir : pip install -r requirements.txt --no-cache-dir"
            echo "   3. Vérifiez le contenu du fichier requirements.txt"
            
            exit 1
        else
            echo -e "${YELLOW}⚠️  Tentative $i échouée, nouvelle tentative dans 5 secondes...${NC}"
            
        fi
    fi
done

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              Lancement de l'analyse
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
pause_for_reading

# Vérifier que le fichier main.py existe
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}❌ Erreur : Le fichier src/main.py n'existe pas${NC}"
    echo -e "${BLUE} Structure attendue du projet :${NC}"
    echo "   └─ src/"
    echo "      └─ main.py"
    exit 1
fi

# Ajouter cette fonction après les autres fonctions
check_monetdb_status() {
    echo -e "${BLUE}📊 Vérification du statut de MonetDB...${NC}"


    # 1. Arrêter tous les processus MonetDB existants
    pkill -f monetdbd

    # 2. Nettoyer et recréer le répertoire de données
    echo -e "${BLUE}🔄 Réinitialisation de MonetDB...${NC}"
    rm -rf ./data/monetdb
    mkdir -p ./data/monetdb
    monetdbd create ./data/monetdb
    monetdbd set port=50000 ./data/monetdb
    
    # 3. Démarrer le serveur
    echo -e "${BLUE}🚀 Démarrage du serveur MonetDB...${NC}"
    monetdbd start ./data/monetdb

    # 4. Créer et configurer la base de données
    echo -e "${BLUE}📦 Création de la base de données ${MONETDB_DB}...${NC}"
    monetdb -q create "${MONETDB_DB}"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erreur lors de la création de la base de données${NC}"
        return 1
    fi
    
    monetdb -q release "${MONETDB_DB}"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erreur lors de la libération de la base de données${NC}"
        return 1
    fi
    
    # 5. Démarrer la base de données
    echo -e "${BLUE}🔄 Démarrage de la base de données ${MONETDB_DB}...${NC}"
    monetdb -q start "${MONETDB_DB}"


    # 6. Vérifier le statut
    if monetdb -q status | grep "${MONETDB_DB}" | grep -q "R"; then
        echo -e "${GREEN}✓ MonetDB est configuré et démarré${NC}"
        echo -e "${BLUE}📊 Informations de connexion MonetDB :${NC}"
        echo "   1. URL : ${MONETDB_DB}"
        echo "   2. Port : 50000"
        echo "   3. Utilisateur : ${MONETDB_USER}"
        echo "   4. Mot de passe : ${MONETDB_PASSWORD}"
    else
        echo -e "${RED}❌ Erreur lors du démarrage de MonetDB${NC}"
        return 1
    fi
}

# Ajouter cette vérification avant le lancement de main.py
echo -e "${BLUE}🔄 Vérification des services de base de données...${NC}"

# Vérifier MonetDB
if ! check_monetdb_status; then
    echo -e "${RED}❌ Erreur lors du démarrage de MonetDB${NC}"
    exit 1
fi

# Fonction pour exécuter une commande avec timeout
run_with_timeout() {
    local cmd="$1"
    local timeout="$2"
    local message="$3"
    
    echo -e "${BLUE}$message${NC}"
    
    # Lancer la commande en arrière-plan
    eval "$cmd" &
    local pid=$!
    
    # Attendre le timeout
    local count=0
    while kill -0 $pid 2>/dev/null; do
        if [ $count -ge $timeout ]; then
            echo -e "${RED}❌ Timeout après $timeout secondes${NC}"
            kill -9 $pid 2>/dev/null
            return 1
        fi
        sleep 1
        ((count++))
        echo -n "."
    done
    
    wait $pid
    return $?
}

# Modifier la section de lancement de main.py
echo -e "${BLUE}🚀 Lancement de main.py...${NC}"


# Exécuter avec timeout de 30 secondes
if ! run_with_timeout "python3 src/main.py" 30 "Exécution du programme principal (timeout 30s)"; then
    echo -e "${RED}❌ Le programme a été interrompu car il prenait trop de temps${NC}"
    echo -e "${BLUE}💡 Suggestions :${NC}"
    echo "   1. Vérifiez les logs pour plus de détails"
    echo "   2. Augmentez le timeout si nécessaire"
    echo "   3. Vérifiez que le programme ne contient pas de boucle infinie"
    
    # Nettoyage des processus Python restants
    pkill -f "python3 src/main.py"
    exit 1
fi

echo -e "${GREEN}✓ Programme exécuté avec succès${NC}"

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ✅ Analyse terminée !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Désactiver l'environnement virtuel
deactivate 