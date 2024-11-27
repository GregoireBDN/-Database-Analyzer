import numpy as np
from tqdm import tqdm
from src.database.postgres_connector import PostgresConnector
from src.database.monetdb_connector import MonetDBConnector
from src.database.postgres_analyzer import PostgresAnalyzer
from src.database.monetdb_analyzer import MonetDBAnalyzer
from src.database.postgres_loader import PostgresLoader
from src.database.monetdb_loader import MonetDBLoader

def analyze_database_performance(queries: list[str], csv_paths: list[tuple[str, str]] = None, iterations: int = 50):
    """
    Analyse les performances des requêtes sur PostgreSQL et MonetDB
    """
    # Initialisation des connecteurs
    pg_connector = PostgresConnector()
    monet_connector = MonetDBConnector()
    
    # Initialisation des analyzers
    pg_analyzer = PostgresAnalyzer(pg_connector)
    monet_analyzer = MonetDBAnalyzer(monet_connector)
    
    # Initialiser results_loader comme une liste vide par défaut
    results_loader = []
    
    # Si un fichier CSV est fourni, chargement des données
    if csv_paths:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("             Chargement des Données")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        pg_loader = PostgresLoader(pg_connector)
        monet_loader = MonetDBLoader(monet_connector)
        
        for path, table_name in csv_paths:
            pg_metrics = pg_loader.load_csv(path, table_name)
            monet_metrics = monet_loader.load_csv(path, table_name)
            
            results_loader.append({
                'table_name': table_name,
                'rows': pg_metrics['total_rows'],
                'pg_load_time': round(pg_metrics['load_time'], 2),
                'monet_load_time': round(monet_metrics['load_time'], 2),
                'ratio': round(monet_metrics['load_time'] / (pg_metrics['load_time'] or 0.001), 2)
            })
        
        print("\n📊 Résumé du chargement :")
        for result in results_loader:
            print(f"\n{result['table_name']} ({result['rows']:,} lignes)")
            print(f"├─ PostgreSQL : {result['pg_load_time']}s")
            print(f"└─ MonetDB   : {result['monet_load_time']}s (x{result['ratio']})")
        
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Analyse des requêtes avec plusieurs itérations
    results_analyzer = []
    total_queries = len(queries)
    
    # Déterminer le nom de la table à partir de la première requête
    table_name = queries[0].lower().split('from')[1].split()[0].strip() if queries else "inconnue"
    
    print(f"\n⏳ Exécution des requêtes pour la table '{table_name}'...")
    for i, query in enumerate(queries, 1):
        pg_times = []
        monet_times = []
        pg_reads = []
        monet_reads = []
        
        print(f"\n Requête {i}/{total_queries} sur {table_name}")
        print(f"└─ Exécution de {iterations} itérations")
        
        with tqdm(total=iterations, unit='iter', ncols=80) as pbar:
            for _ in range(iterations):
                pg_metrics = pg_analyzer.analyze_query(query)
                pg_times.append(pg_metrics['execution_time'])
                pg_reads.append(pg_metrics['physical_reads'])
                
                monet_metrics = monet_analyzer.analyze_query(query)
                monet_times.append(monet_metrics['execution_time'])
                monet_reads.append(monet_metrics['physical_reads'])
                
                pbar.update(1)
        
        comparison = {
            'query_id': i,
            'query': query,
            'pg_execution_time': {
                'mean': np.mean(pg_times),
                'min': np.min(pg_times),
                'max': np.max(pg_times),
                'std': np.std(pg_times)
            },
            'monet_execution_time': {
                'mean': np.mean(monet_times),
                'min': np.min(monet_times),
                'max': np.max(monet_times),
                'std': np.std(monet_times)
            },
            'pg_physical_reads': {
                'mean': np.mean(pg_reads),
                'min': np.min(pg_reads),
                'max': np.max(pg_reads),
                'std': np.std(pg_reads)
            },
            'monet_physical_reads': {
                'mean': np.mean(monet_reads),
                'min': np.min(monet_reads),
                'max': np.max(monet_reads),
                'std': np.std(monet_reads)
            }
        }
        results_analyzer.append(comparison)
    
    return results_analyzer 