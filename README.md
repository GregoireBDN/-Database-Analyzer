# 📊 Database Analyzer

## 📋 Table des matières

1. [Introduction](#-introduction)
2. [Auteurs](#-auteurs)
3. [Objectifs](#-objectifs-du-projet)
4. [Prérequis et Données](#-prérequis-et-données)
   - [Prérequis système](#prérequis-système)
   - [Données requises](#données-requises)
5. [Installation](#-installation)
   - [Installation rapide](#-installation-rapide)
   - [Installation détaillée](#-installation-détaillée)
6. [Structure du projet](#-structure-du-projet)
7. [Fonctionnalités](#-fonctionnalités)
   - [Configuration automatique](#configuration-automatique)
   - [Analyse des performances](#analyse-des-performances)
   - [Visualisation](#visualisation)
8. [Résultats](#-résultats)
9. [Licence](#-licence)

## 📝 Introduction

Ce projet d'analyse comparative de bases de données a été développé dans le cadre de l'UE "Bases de Données" du Master Ingénierie Logicielle à l'Université de Rennes. Il permet d'évaluer et de comparer les performances de PostgreSQL et MonetDB sur différents types de requêtes et scénarios d'utilisation.

L'outil propose une suite complète de tests automatisés, générant des visualisations détaillées et des métriques précises pour faciliter la comparaison des performances entre ces deux SGBD.

### 🌟 Points forts

- Analyse comparative approfondie
- Installation automatisée via Docker
- Visualisations graphiques détaillées
- Tests sur différents types de requêtes
- Documentation complète

## 👥 Auteurs

- **Grégoire BODIN** - Master 1 IL
- **Léo BERNARD-BORDIER** - Master 1 IL

## 🎯 Objectifs du Projet

Ce projet vise à :

- Comparer les performances de PostgreSQL et MonetDB
- Analyser l'impact des différentes stratégies d'indexation
- Évaluer les performances sur différents types de requêtes :
  - Requêtes de sélection simple
  - Jointures complexes
  - Agrégations
- Fournir des visualisations claires et détaillées des résultats

## 📋 Prérequis et Données

### Prérequis système

- Git
- Docker et Docker Compose
- 4 Go de RAM minimum
- 2 Go d'espace disque disponible

Le script d'installation s'occupera automatiquement de :

- La création des conteneurs Docker
- L'installation des SGBD
- La configuration de l'environnement
- L'importation des données de test

### Données requises

En raison de leur taille, les fichiers de données ne sont pas inclus directement dans le dépôt. Vous devez les télécharger séparément :

#### Sources des données

- **Air Quality Data** : [NYC Open Data - Air Quality](https://catalog.data.gov/dataset/air-quality)

  - Description : Données de surveillance de la qualité de l'air à New York
  - Format : CSV

- **Crime Data** : [LA City - Crime Data 2020 to Present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)
  - Description : Données sur la criminalité à Los Angeles depuis 2020
  - Format : CSV

## 🚀 Installation

### Installation rapide

1. **Cloner le repository**

   ```bash
   git clone git@github.com:GregoireBDN/Database-Analyzer.git
   cd Database-Analyzer
   ```

2. **Configurer l'environnement**

   ```bash
   cp .env.example .env
   # Modifier les variables dans .env si nécessaire
   ```

3. **Lancer l'installation et l'analyse**

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

4. **Installation des données**

5. Créer le dossier `data` s'il n'existe pas :

```bash
mkdir -p data
```

2. Télécharger les fichiers CSV et les placer dans le dossier `data/`

3. Vérifier que les fichiers sont correctement nommés :

- `data/air_quality.csv`
- `data/crimes.csv`

Note : Ces fichiers sont nécessaires pour exécuter les analyses. Le dossier `data/` est ignoré par Git en raison de la taille des fichiers.

### Installation détaillée

1. **Configuration de l'environnement**

   - Copier `.env.example` vers `.env`
   - Ajuster les paramètres selon vos besoins :
     - Ports des bases de données
     - Identifiants de connexion
     - Taille des lots de données

2. **Préparation des données**

   1. Créer le dossier `data` s'il n'existe pas :

   ```bash
   mkdir -p data
   ```

3. Télécharger les fichiers CSV et les placer dans le dossier `data/`

4. Vérifier que les fichiers sont correctement nommés :

- `data/air_quality.csv`
- `data/crimes.csv`

Note : Ces fichiers sont nécessaires pour exécuter les analyses. Le dossier `data/` est ignoré par Git en raison de la taille des fichiers.

3. **Lancement des services**

   ```bash
   docker compose up -d
   ```

4. **Vérification de l'installation**
   ```bash
   docker compose ps
   ```

## 📁 Structure du projet

```
Database-Analyzer/
├── docker/                 # Configurations Docker
│   ├── python/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── postgres/
│   │   └── Dockerfile
│   └── monetdb/
│       ├── Dockerfile
│       └── scripts/
│           └── start-monetdb.sh
├── scripts/               # Scripts utilitaires
│   └── init.sh           # Script principal
├── src/                  # Code source Python
│   ├── database/        # Connecteurs, loaders et analyseurs
│   ├── queries/         # Requêtes SQL
│   ├── visualization/   # Génération des graphiques
│   ├── __init__.py
│   └── main.py         # Point d'entrée
├── data/                # Données d'analyse
│   ├── air_quality.csv
│   └── crime.csv
├── results/            # Graphiques générés
├── run.sh              # Script de lancement
├── setup.py           # Configuration du package
├── docker-compose.yml # Configuration des services
├── .env.example       # Template des variables d'environnement
└── README.md         # Documentation
```

## 🔍 Fonctionnalités

- **Configuration automatique**

  - Installation des SGBD
  - Création des bases de données
  - Configuration des utilisateurs et permissions

- **Analyse des performances**

  - Temps d'exécution des requêtes
  - Utilisation des ressources
  - Lecture/écriture disque
  - Impact des index

- **Visualisation**
  - Graphiques comparatifs
  - Statistiques détaillées
  - Export des résultats

## 📊 Résultats

Les résultats de l'analyse sont générés dans le dossier `results/` et incluent :

- Graphiques de comparaison des temps d'exécution
- Rapports détaillés par type de requête

## 🛠 Aperçu des Résultats

### Analyse de la Qualité de l'Air

![Analyse Qualité Air](results/air_quality_performance.png)

Les résultats montrent que :

- PostgreSQL est plus efficace pour le chargement initial (0.03 ms/ligne vs 0.22 ms/ligne pour MonetDB)
- Les requêtes de sélection (Q1) et d'agrégation (Q2) sont similaires en performance
- MonetDB montre des performances inférieures sur les jointures complexes (Q3) avec un temps d'exécution ~7x plus élevé

### Analyse des Crimes

![Analyse Crimes](results/crimes_performance.png)

Points clés :

- MonetDB montre un temps de chargement plus élevé (0.37 ms/ligne vs 0.05 ms/ligne pour PostgreSQL)
- PostgreSQL présente des temps d'exécution significativement plus élevés pour :
  - Les agrégations (Q2) : ~400ms vs ~15ms pour MonetDB
  - Les jointures (Q3) : ~325ms vs ~20ms pour MonetDB
- MonetDB maintient des performances constantes sur tous les types de requêtes

### Conclusions

1. **Chargement des données** :

   - PostgreSQL est plus efficace pour le chargement initial des données
   - MonetDB montre des temps de chargement 7-8x plus élevés

2. **Exécution des requêtes** :
   - MonetDB excelle dans les opérations d'agrégation et de jointure sur grands volumes
   - PostgreSQL performe mieux sur les requêtes de sélection simples
   - Les différences de performance sont plus marquées sur le jeu de données "Crimes" (plus volumineux)

## 📝 Licence

Ce projet a été développé dans un cadre universitaire à l'Université de Rennes.
