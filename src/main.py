import os
os.environ['PYTHON_CODESIGN_IDENTITY'] = '-'

from src.queries.air_quality_queries import AIR_QUALITY_QUERIES
from src.queries.crimes_queries import CRIMES_QUERIES
from src.config import CSV_PATHS, GRAPH_CONFIG
from src.visualization import create_performance_graph
from src.database.performance_analyzer import analyze_database_performance

def main():
    # Analyse des performances pour chaque ensemble de requêtes
    results_air_quality = analyze_database_performance(
        AIR_QUALITY_QUERIES, 
        csv_paths=CSV_PATHS, 
        iterations=50
    )
    
    results_crimes = analyze_database_performance(
        CRIMES_QUERIES, 
        iterations=50
    )
    
    # Création des graphiques
    create_performance_graph(results_air_quality, GRAPH_CONFIG['air_quality'])
    create_performance_graph(results_crimes, GRAPH_CONFIG['crimes'])

if __name__ == "__main__":
    main()
