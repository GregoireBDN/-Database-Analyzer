# Configuration des chemins
CSV_PATHS = [
    ("data/air_quality.csv", "air_quality"),
    ("data/crimes.csv", "crimes")
]

# Configuration des graphiques
GRAPH_CONFIG = {
    'air_quality': {
        'title': 'Performances des requêtes - Air Quality',
        'query_names': ['Requête 1', 'Requête 2', 'Requête 3', 'Requête 4', 'Requête 5'],
        'output_path': 'results/air_quality_performance.png',
        'loading_times': {
            'postgres': 0.0,  # temps en ms
            'monetdb': 0.0    # temps en ms
        }
    },
    'crimes': {
        'query_names': [
            'COUNT\nTotal',
            'Analyse\npar Zone',
            'Stats par\nType Crime',
            'Analyse\nTemporelle',
            'Analyse\nGéographique'
        ],
        'output_path': 'results/performance_comparison_crimes.png',
        'title': 'Comparaison des temps d\'exécution - Crimes'
    }
}