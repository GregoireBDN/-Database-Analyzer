# 📊 Database Analyzer

## 📋 Table des matières

1. [Introduction](#-introduction)
2. [Auteurs](#-auteurs)
3. [Objectifs](#-objectifs-du-projet)
4. [Installation](#-installation)
   - [Prérequis système](#prérequis-système)
   - [Installation du projet](#installation-du-projet)
   - [Installation des données](#installation-des-données)
   - [Lancement de l'analyse](#lancement-de-lanalyse)
5. [Structure du projet](#-structure-du-projet)
6. [Fonctionnalités](#-fonctionnalités)
   - [Configuration automatique](#configuration-automatique)
   - [Analyse des performances](#analyse-des-performances)
   - [Visualisation](#visualisation)
7. [Résultats](#-résultats)
8. [Licence](#-licence)

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

## 🚀 Installation

### Prérequis système

- Git
- Docker et Docker Compose
- 4 Go de RAM minimum
- 2 Go d'espace disque disponible

### Installation du projet

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

### Installation des données

En raison de leur taille, les fichiers de données doivent être téléchargés séparément :

#### Sources des données

- **Air Quality Data** : [NYC Open Data - Air Quality](https://catalog.data.gov/dataset/air-quality)

  - Description : Données de surveillance de la qualité de l'air à New York
  - Format : CSV
  - Placer dans : `data/air_quality.csv`

- **Crime Data** : [LA City - Crime Data 2020 to Present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)
  - Description : Données sur la criminalité à Los Angeles depuis 2020
  - Format : CSV
  - Placer dans : `data/crimes.csv`

#### Préparation des données

1. Créer le dossier `data` :
   ```bash
   mkdir -p data
   ```
2. Télécharger et placer les fichiers CSV dans `data/`
3. Vérifier les noms des fichiers :
   - `data/air_quality.csv`
   - `data/crimes.csv`

### Lancement de l'analyse

Une fois les données installées :

```bash
chmod +x run.sh
./run.sh
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
  - Les sélections (Q1) : ~100ms vs ~15ms pour MonetDB
  - Les agrégations (Q2) : ~400ms vs ~15ms pour MonetDB
  - Les jointures (Q3) : ~325ms vs ~20ms pour MonetDB
- MonetDB maintient des performances constantes sur tous les types de requêtes

### Conclusions

1. **Chargement des données** :

   - PostgreSQL est plus efficace pour le chargement initial des données
   - MonetDB montre des temps de chargement 7-8x plus élevés

2. **Exécution des requêtes** :

   - PostgreSQL performe mieux sur des requêtes de jointure sur un faible volume de données

   - MonetDB excelle sur l'ensemble des requêtes avec des volumes de données plus importants

## 📝 Licence

Ce projet a été développé dans un cadre universitaire à l'Université de Rennes.
