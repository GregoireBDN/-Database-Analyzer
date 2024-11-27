#!/bin/bash

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Mettre à jour pip dans l'environnement virtuel
echo -e "${BLUE}📥 Mise à jour de pip...${NC}"
python3 -m pip install --upgrade pip

# Installer les dépendances
echo -e "${BLUE}📥 Installation des dépendances...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dépendances installées${NC}"

echo -e "${BLUE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              Lancement de l'analyse
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Lancer le programme principal
python3 src/main.py

# Vérifier si l'exécution s'est bien passée
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'exécution du programme${NC}"
    exit 1
fi

echo -e "${GREEN}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ✅ Analyse terminée !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Désactiver l'environnement virtuel
deactivate 