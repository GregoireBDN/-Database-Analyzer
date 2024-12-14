# 📊 Database Analyzer

## 📋 Table des matières

1. [Introduction](#-introduction)
2. [Auteurs](#-auteurs)
3. [Objectifs](#-objectifs-du-projet)
4. [Prérequis](#-prérequis)
5. [Installation](#-installation)
   - [Installation rapide](#-installation-rapide)
   - [Installation détaillée](#-installation-détaillée)
6. [Structure du projet](#-structure-du-projet)
7. [Fonctionnalités](#-fonctionnalités)
   - [Configuration automatique](#configuration-automatique)
   - [Analyse des performances](#analyse-des-performances)
   - [Visualisation](#visualisation)
8. [Résultats](#-résultats)
9. [Dépannage](#-dépannage)

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
  - Requêtes temporelles
- Fournir des visualisations claires et détaillées des résultats

## 📋 Prérequis

- Git
- Docker et Docker Compose
- 4 Go de RAM minimum
- 2 Go d'espace disque disponible

Le script d'installation s'occupera automatiquement de :

- La création des conteneurs Docker
- L'installation des SGBD
- La configuration de l'environnement
- L'importation des données de test

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

### Installation détaillée

1. **Configuration de l'environnement**

   - Copier `.env.example` vers `.env`
   - Ajuster les paramètres selon vos besoins :
     - Ports des bases de données
     - Identifiants de connexion
     - Taille des lots de données

2. **Préparation des données**

   - Placer vos fichiers CSV dans le dossier `data/`
   - Format attendu :
     - air_quality.csv : données de qualité de l'air
     - crimes.csv : données de criminalité

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

## 🛠 Dépannage

En cas de problèmes, vérifiez les points suivants :

| Problème              | Solution                                              |
| --------------------- | ----------------------------------------------------- |
| Services non démarrés | Vérifiez le statut des services PostgreSQL et MonetDB |
| Erreurs MonetDB       | Consultez `./data/monetdb/merovingian.log`            |
| Ports occupés         | Vérifiez si les ports 5432 et 50000 sont disponibles  |
| Permissions           | Assurez-vous que `./data` a les bonnes permissions    |
| Python non installé   | Le script proposera de l'installer automatiquement    |

## 📫 Support et Contact

Pour toute question ou problème :

1. Consultez la section dépannage ci-dessus
2. Vérifiez les logs des services
3. Ouvrez une issue sur GitHub
4. Contactez les auteurs :
   - Grégoire BODIN (gregoire.bodin@etu.univ-nantes.fr)
   - Léo BERNARD-BORDIER (leo.bernard-bordier@etu.univ-nantes.fr)

## 📝 Licence

Ce projet a été développé dans un cadre universitaire à l'Université de Rennes.

## 🔍 Fonctionnalités détaillées

### Configuration automatique

- Installation et configuration des SGBD
- Création des bases de données et des tables
- Import automatique des données
- Configuration des index et optimisations

### Analyse des performances

- Mesure précise des temps d'exécution
- Analyse de l'utilisation des ressources
- Comparaison des stratégies d'indexation
- Tests de charge et de concurrence

### Visualisation

- Graphiques comparatifs détaillés
- Export des résultats en PNG
- Métriques détaillées par type de requête
- Analyse des temps de chargement

## 📊 Résultats

Les résultats sont générés dans le dossier `results/` et comprennent :

- **Graphiques de performance**

  - Temps d'exécution par type de requête
  - Comparaison des temps de chargement
  - Impact des index sur les performances

- **Rapports détaillés**
  - Métriques par requête
  - Statistiques d'utilisation des ressources
  - Analyse comparative complète

## 🛠 Dépannage

| Problème              | Solution                       |
| --------------------- | ------------------------------ |
| Services non démarrés | `docker compose restart`       |
| Erreurs de connexion  | Vérifier les ports dans `.env` |
| Problèmes de données  | Vérifier les fichiers CSV      |
| Manque de mémoire     | Augmenter la RAM Docker        |
