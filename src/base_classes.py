from abc import ABC, abstractmethod
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DatabaseConnector(ABC):
    def __init__(self):
        self.user = None
        self.password = None
        self.host = None
        self.database = None
        self.port = None
        self.connection = None
        self._load_env_vars()
    
    @abstractmethod
    def _load_env_vars(self):
        """Charge les variables d'environnement"""
        pass
        
    @abstractmethod
    def connect(self):
        """Établit la connexion"""
        pass
    
    @abstractmethod
    def get_connection(self):
        """Retourne la connexion active"""
        pass

class DatabaseLoader(ABC):
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.strip().replace(' ', '_').replace('-', '_').lower() 
                     for col in df.columns]
        return df
    
    @abstractmethod
    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000) -> None:
        """Charge un fichier CSV dans la base"""
        pass

class QueryAnalyzer(ABC):
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector
    
    @abstractmethod
    def analyze_query(self, query: str) -> Dict:
        """Analyse une requête"""
        pass
    
    def analyze_multiple_queries(self, queries: List[str]) -> List[Dict]:
        """Analyse plusieurs requêtes"""
        results = []
        for i, query in enumerate(queries, 1):
            metrics = self.analyze_query(query)
            if metrics:
                results.append(metrics)
        return results

    def format_metrics(self, metrics: Dict) -> Dict:
        """Formate les métriques de manière uniforme"""
        return {
            'query': metrics['query'],
            'execution_time': float(metrics['execution_time']),
            'row_count': int(metrics['row_count']),
            'physical_reads': int(metrics.get('physical_reads', 0)),
            'physical_writes': int(metrics.get('physical_writes', 0))
        }