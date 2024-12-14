import numpy as np
from tqdm import tqdm
from src.database.postgres_connector import PostgresConnector
from src.database.monetdb_connector import MonetDBConnector
from src.database.postgres_analyzer import PostgresAnalyzer
from src.database.monetdb_analyzer import MonetDBAnalyzer
from src.database.postgres_loader import PostgresLoader
from src.database.monetdb_loader import MonetDBLoader
import logging

logger = logging.getLogger(__name__)

def analyze_database_performance(
    queries: list[str], 
    csv_paths: list[tuple[str, str]] = None, 
    iterations: int = 50,
    table_name: str = None,
    config: dict = None
) -> tuple[list[dict], list[dict]]:
    """
    Analyse les performances des requêtes sur PostgreSQL et MonetDB
    
    Args:
        queries: Liste des requêtes à analyser
        csv_paths: Liste des chemins CSV et noms de tables associés
        iterations: Nombre d'itérations pour chaque requête
        table_name: Nom de la table pour l'analyse
        config: Configuration pour les graphiques
        
    Returns:
        Tuple contenant les résultats d'analyse et les métriques de chargement
    """
    if config is None:
        config = {}  # Initialisation d'un dictionnaire vide si config est None
    
    logger.info(f"Démarrage de l'analyse pour la table {table_name}")
    
    # Validation des paramètres
    if not queries:
        raise ValueError("La liste des requêtes ne peut pas être vide")
    
    if iterations < 1:
        raise ValueError("Le nombre d'itérations doit être positif")
    
    # Filtrer les CSV paths pour ne charger que la table demandée
    if table_name and csv_paths:
        csv_paths = [(path, name) for path, name in csv_paths if name == table_name]
        if not csv_paths:
            raise ValueError(f"Aucun fichier CSV trouvé pour la table {table_name}")
    
    try:
        # Initialisation des connecteurs avec gestion d'erreur
        pg_connector = PostgresConnector()
        monet_connector = MonetDBConnector()
        
        # Tentative de connexion
        pg_connector.connect()
        monet_connector.connect()
        
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
                    'ratio': round(monet_metrics['load_time'] / (pg_metrics['load_time'] or 0.001), 2),
                    'load_per_row': {
                        'pg': round((pg_metrics['load_time'] * 1000) / pg_metrics['total_rows'], 4),  # ms/ligne
                        'monet': round((monet_metrics['load_time'] * 1000) / pg_metrics['total_rows'], 4)
                    }
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
        
        print(f"\n⏳ Exécution des requêtes...")
        for i, query in enumerate(queries, 1):
            pg_times = []
            monet_times = []
            
            print(f"\n Requête {i}/{total_queries}")
            print(f"└─ Exécution de {iterations} itérations")
            
            with tqdm(total=iterations, unit='iter', ncols=80) as pbar:
                for _ in range(iterations):
                    try:
                        # Exécution PostgreSQL
                        pg_metrics = pg_analyzer.analyze_query(query)
                        if 'error' not in pg_metrics:
                            pg_times.append(pg_metrics['execution_time'])
                        
                        # Exécution MonetDB
                        monet_metrics = monet_analyzer.analyze_query(query)
                        if 'error' not in monet_metrics:
                            monet_times.append(monet_metrics['execution_time'])
                            
                    except Exception as e:
                        print(f"\nErreur lors de l'exécution: {str(e)}")
                        continue
                        
                    pbar.update(1)
            
            # Vérification qu'il y a des résultats valides
            if pg_times and monet_times:
                comparison = {
                    'query_id': i,
                    'query': query,
                    'pg_execution_time': {
                        'mean': float(np.mean(pg_times)),
                        'min': float(np.min(pg_times)),
                        'max': float(np.max(pg_times))
                    },
                    'monet_execution_time': {
                        'mean': float(np.mean(monet_times)), 
                        'min': float(np.min(monet_times)),
                        'max': float(np.max(monet_times))
                    }
                }
                results_analyzer.append(comparison)
            else:
                print(f"\n⚠️ Aucun résultat valide pour la requête {i}")
        
        if csv_paths and results_loader:
            config['loading_times'] = {
                'pg_load_time': results_loader[0]['pg_load_time'],
                'monet_load_time': results_loader[0]['monet_load_time']
            }
            config['total_rows'] = results_loader[0]['rows']
        
        return results_analyzer, results_loader
    
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation : {str(e)}")
        raise