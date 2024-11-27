# 📊 Database Analyzer

Ce projet a été développé dans le cadre de l'UE "Bases de Données Avancées" du Master Ingénierie Logicielle à l'Université de Nantes. Il permet d'analyser et de comparer les performances de PostgreSQL et MonetDB sur différents types de requêtes.

## 👥 Auteurs

- **Grégoire BODIN** - Master 2 IL
- **Léo BERNARD-BORDIER** - Master 2 IL

## 🎯 Objectifs du Projet

Ce projet vise à :

- Comparer les performances de PostgreSQL et MonetDB
- Analyser l'impact des différentes stratégies d'indexation
- Évaluer les performances sur différents types de requêtes :
  - Requêtes de sélection simple
  - Jointures complexes
  - Agrégations
  - Requêtes temporelles
- Visualiser les résultats via des graphiques comparatifs

## 📋 Table des matières

- [Prérequis](#-prérequis)
- [Installation rapide](#-installation-rapide)
- [Installation détaillée](#️-installation-détaillée)
- [Structure du projet](#-structure-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Résultats](#-résultats)
- [Dépannage](#-dépannage)

## 🔧 Prérequis

- Git
- Droits administrateur (pour l'installation des dépendances)

Le script d'installation s'occupera d'installer automatiquement :

- Python 3.11+
- PostgreSQL 15
- MonetDB
- Toutes les dépendances Python nécessaires

## 🚀 Installation rapide

1. **Cloner le repository**

   ```bash
   git clone git@github.com:GregoireBDN/Database-Analyzer.git
   cd Database-Analyzer
   ```

2. **Lancer l'installation et l'analyse**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## 📁 Structure du projet

```
Database-Analyzer/
├── src/
│   ├── database/           # Connecteurs et analyseurs de BDD
│   ├── visualization/      # Génération des graphiques
│   └── main.py            # Point d'entrée du programme
├── data/                   # Données d'analyse
├── results/               # Graphiques générés
├── requirements.txt       # Dépendances Python
├── setup_databases.sh     # Script de configuration des BDD
├── run_analysis.sh        # Script d'analyse
└── run.sh                # Script principal
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
- Statistiques sur l'utilisation des ressources
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
