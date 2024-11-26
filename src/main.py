import pandas as pd
from src.postgres.postgres_connector import PostgresConnector
from src.postgres.postgres_loader import PostgresLoader
from src.postgres.postgres_analyzer import PostgresAnalyzer
from src.monetdb.monetdb_connector import MonetDBConnector
from src.monetdb.monetdb_loader import MonetDBLoader
from src.monetdb.monetdb_analyzer import MonetDBAnalyzer

def analyze_database_performance(queries: list[str], csv_paths: list[tuple[str, str]] = None):
    """
    Analyse les performances des requêtes sur PostgreSQL et MonetDB
    """
    # Initialisation des connecteurs
    pg_connector = PostgresConnector()
    monet_connector = MonetDBConnector()
    
    # Initialisation des analyzers
    pg_analyzer = PostgresAnalyzer(pg_connector)
    monet_analyzer = MonetDBAnalyzer(monet_connector)
    
    # Si un fichier CSV est fourni, chargement des données
    if csv_paths:
        print("Chargement des données...")
        pg_loader = PostgresLoader(pg_connector)
        monet_loader = MonetDBLoader(monet_connector)
        results_loader = []
        
        for path, table_name in csv_paths:
            pg_load_metrics = pg_loader.load_csv(path, table_name)
            monet_load_metrics = monet_loader.load_csv(path, table_name)
            print(f"Chargement de {table_name} terminé en {pg_load_metrics['load_time']} secondes sur PostgreSQL et {monet_load_metrics['load_time']} secondes sur MonetDB")
            results_loader.append({
                'table_name': table_name,
                'pg_load_time': pg_load_metrics['load_time'],
                'monet_load_time': monet_load_metrics['load_time']
            })
        print("Données chargées avec succès!")
    
    # Analyse des requêtes
    results_analyzer = []
    for i, query in enumerate(queries, 1):
        print(f"\nAnalyse de la requête {i}:")
        print(f"SQL: {query}")
        
        # Exécution sur PostgreSQL
        pg_metrics = pg_analyzer.analyze_query(query)
        
        # Exécution sur MonetDB
        monet_metrics = monet_analyzer.analyze_query(query)
        
        # Comparaison des résultats
        comparison = {
            'query_id': i,
            'query': query,
            'pg_execution_time': pg_metrics['execution_time'],
            'monet_execution_time': monet_metrics['execution_time'],
            'pg_row_count': pg_metrics['row_count'],
            'monet_row_count': monet_metrics['row_count'],
            'pg_physical_reads': pg_metrics['physical_reads'],
            'monet_physical_reads': monet_metrics['physical_reads'],
            'time_ratio': monet_metrics['execution_time'] / pg_metrics['execution_time']
        }
        results_analyzer.append(comparison)
    
    return pd.DataFrame(results_analyzer), pd.DataFrame(results_loader)

def main():
    # Utilisation de la fonction analyze_database_performance
    csv_paths = [("data/air_quality.csv", "air_quality"), ("data/crimes.csv", "crimes")]
    
    test_queries = [
        "SELECT COUNT(*) FROM crimes GROUP BY (SELECT SUBSTRING('10/10/2020 12:00:00 AM', 7, 4))"
    ]
    
    # Appel de la fonction d'analyse
    results_df, loader_df = analyze_database_performance(test_queries, csv_paths)
    
    # Affichage des résultats
    print("\nRésultats du chargement des données:")
    print(loader_df)
    print("\nRésultats de l'analyse des requêtes:")
    print(results_df)

if __name__ == "__main__":
    main()
