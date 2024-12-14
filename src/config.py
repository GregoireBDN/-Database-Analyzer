"""
Configuration du système d'analyse de performances des bases de données.

Ce module contient les configurations nécessaires pour :
    - Les chemins des fichiers de données
    - Les paramètres de visualisation des graphiques
    - Les métriques de performance pour chaque jeu de données

Structure:
---------
Le fichier est organisé en deux parties principales :
1. Configuration des chemins des données
2. Configuration des graphiques et métriques
"""

# Configuration des chemins des données
CSV_PATHS = [
    ("data/air_quality.csv", "air_quality"),
    ("data/crimes.csv", "crimes")
]

# Configuration des graphiques et métriques de performance
GRAPH_CONFIG = {
    'air_quality': {
        'title': 'Analyse de Performance - Qualité de l\'Air',
        'output_file': 'air_quality_performance.png',
        'loading_times': {
            'pg_load_time': 0.0,
            'monet_load_time': 0.0
        },
        'total_rows': 0
    },
    'crimes': {
        'title': 'Analyse de Performance - Crimes',
        'output_file': 'crimes_performance.png',
        'loading_times': {
            'postgres': 0.0,
            'monetdb': 0.0
        }
    }
}

"""
Utilisation:
-----------
Pour utiliser cette configuration:

1. Accès aux chemins des fichiers:
    from config import CSV_PATHS
    for path, table_name in CSV_PATHS:
        # Traitement des fichiers

2. Accès à la configuration des graphiques:
    from config import GRAPH_CONFIG
    air_quality_config = GRAPH_CONFIG['air_quality']
    crimes_config = GRAPH_CONFIG['crimes']

3. Mise à jour des temps de chargement:
    GRAPH_CONFIG['air_quality']['loading_times']['postgres'] = measured_time

Notes:
------
- Les temps de chargement sont initialisés à 0.0 et sont mis à jour
  pendant l'exécution du programme
- Les noms des requêtes doivent correspondre à l'ordre des requêtes
  dans les fichiers de requêtes respectifs
- Les chemins de sortie sont relatifs au répertoire racine du projet
"""