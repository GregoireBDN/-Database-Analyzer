"""
Module principal pour l'analyse comparative des performances entre PostgreSQL et MonetDB.

Ce module coordonne l'exécution des tests de performance, le chargement des données,
et la génération des graphiques de comparaison. Il utilise les configurations définies
dans config.py et les requêtes spécifiées dans les modules queries.

Fonctionnalités principales:
    - Chargement et analyse des données de qualité de l'air
    - Chargement et analyse des données de crimes
    - Génération de graphiques comparatifs
    - Affichage des métriques détaillées

Dépendances:
    - logging: Pour la journalisation des événements
    - src.queries: Modules contenant les requêtes à analyser
    - src.config: Configuration des chemins et paramètres
    - src.visualization: Création des graphiques
    - src.database.performance_analyzer: Analyse des performances
"""

import os
import sys
from typing import Dict, Any
import logging

# Configuration de l'environnement
os.environ['PYTHON_CODESIGN_IDENTITY'] = '-'

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imports des modules internes
from src.queries.air_quality_queries import AIR_QUALITY_QUERIES
from src.queries.crimes_queries import CRIMES_QUERIES
from src.config import CSV_PATHS, GRAPH_CONFIG
from src.visualization import create_performance_graph
from src.database.performance_analyzer import analyze_database_performance

def main() -> None:
    """
    Fonction principale qui orchestre l'analyse des performances des bases de données.
    
    Cette fonction:
    1. Charge et analyse les données de qualité de l'air
    2. Charge et analyse les données de crimes
    3. Génère des graphiques comparatifs
    4. Affiche un résumé détaillé des performances
    
    Le processus complet inclut:
        - Chargement initial des données depuis les fichiers CSV
        - Exécution des requêtes de test sur les deux bases de données
        - Collecte des métriques de performance
        - Génération des visualisations
        - Affichage des résultats détaillés
    
    Raises:
        Exception: Si une erreur survient pendant l'exécution, elle est capturée,
                  journalisée et provoque l'arrêt du programme avec un code d'erreur.
    
    Note:
        Les résultats sont sauvegardés dans le dossier 'results/' sous forme de
        graphiques PNG et les métriques détaillées sont affichées dans la console.
    """
    try:
        logger.info("Démarrage de l'analyse des performances...")
        
        # Analyse des données de qualité de l'air
        analyzer_air_quality, loader_air_quality = analyze_database_performance(
            AIR_QUALITY_QUERIES, 
            csv_paths=CSV_PATHS,
            table_name="air_quality",
            iterations=50,
            config=GRAPH_CONFIG['air_quality']
        )
        
        # Analyse des données de crimes
        analyzer_crimes, loader_crimes = analyze_database_performance(
            CRIMES_QUERIES, 
            csv_paths=CSV_PATHS,
            table_name="crimes",
            iterations=50,
            config=GRAPH_CONFIG['crimes']
        )
        
        # Mettre à jour les configurations avec les temps réels
        if loader_air_quality:
            GRAPH_CONFIG['air_quality'].update({
                'loading_times': {
                    'pg_load_time': loader_air_quality[0]['pg_load_time'] * 1000,  # Conversion en ms
                    'monet_load_time': loader_air_quality[0]['monet_load_time'] * 1000
                },
                'total_rows': loader_air_quality[0]['rows']
            })

        if loader_crimes:
            GRAPH_CONFIG['crimes'].update({
                'loading_times': {
                    'pg_load_time': loader_crimes[0]['pg_load_time'] * 1000,
                    'monet_load_time': loader_crimes[0]['monet_load_time'] * 1000
                },
                'total_rows': loader_crimes[0]['rows']
            })
        
        # Création des graphiques
        logger.info("Génération des graphiques...")
        if analyzer_air_quality:
            create_performance_graph(analyzer_air_quality, GRAPH_CONFIG['air_quality'])
        if analyzer_crimes:
            create_performance_graph(analyzer_crimes, GRAPH_CONFIG['crimes'])
        
        # Afficher les métriques de chargement
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("                Métriques de l'Analyse")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Affichage des métriques de chargement
        for metrics in loader_air_quality + loader_crimes:
            print(f"\n📊 Table: {metrics['table_name']}")
            print(f"  ├─ Lignes: {metrics['rows']:,}")
            print(f"  ├─ PostgreSQL: {metrics['pg_load_time']:.2f} s")
            print(f"  ├─ MonetDB: {metrics['monet_load_time']:.2f} s")
            print(f"  └─ Ratio MonetDB/PostgreSQL: {metrics['ratio']:.2f}")

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        logger.info("Analyse terminée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()