"""
Classes de base pour la gestion des connexions et du chargement des données.

Ce module définit les classes abstraites qui servent de base pour l'implémentation
des connecteurs de bases de données et des chargeurs de données. Il fournit une
structure commune pour assurer la cohérence entre les différentes implémentations.

Classes:
    - DatabaseConnector: Classe abstraite pour les connecteurs de bases de données
    - DatabaseLoader: Classe abstraite pour les chargeurs de données
    - QueryAnalyzer: Classe abstraite pour les analyseurs de requêtes

Notes:
    Toutes les classes de ce module sont abstraites (ABC) et nécessitent une
    implémentation concrète pour être utilisées.
"""

from abc import ABC, abstractmethod
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DatabaseConnector(ABC):
    """
    Classe abstraite définissant l'interface pour les connecteurs de bases de données.
    
    Cette classe fournit la structure de base pour gérer les connexions aux différentes
    bases de données (PostgreSQL, MonetDB, etc.).

    Attributes:
        user (str): Nom d'utilisateur pour la connexion
        password (str): Mot de passe pour la connexion
        host (str): Hôte de la base de données
        database (str): Nom de la base de données
        port (int): Port de connexion
        connection: Objet de connexion à la base de données

    Methods:
        _load_env_vars(): Charge les variables d'environnement
        connect(): Établit la connexion à la base de données
        get_connection(): Retourne la connexion active
    """

    def __init__(self):
        """
        Initialise les attributs de connexion à None et charge les variables
        d'environnement.
        """
        self.user: Optional[str] = None
        self.password: Optional[str] = None
        self.host: Optional[str] = None
        self.database: Optional[str] = None
        self.port: Optional[int] = None
        self.connection = None
        self._load_env_vars()
    
    @abstractmethod
    def _load_env_vars(self) -> None:
        """
        Charge les variables d'environnement spécifiques à la base de données.
        
        Cette méthode doit être implémentée par les classes enfants pour définir
        quelles variables d'environnement charger et comment les utiliser.
        """
        pass
        
    @abstractmethod
    def connect(self) -> None:
        """
        Établit la connexion à la base de données.
        
        Cette méthode doit être implémentée par les classes enfants pour définir
        comment se connecter à leur base de données respective.
        
        Raises:
            Exception: Si la connexion échoue
        """
        pass
    
    @abstractmethod
    def get_connection(self):
        """
        Retourne la connexion active à la base de données.
        
        Returns:
            Connection: Objet de connexion spécifique à la base de données

        Cette méthode doit être implémentée par les classes enfants pour retourner
        le bon type de connexion.
        """
        pass

class DatabaseLoader(ABC):
    """
    Classe abstraite définissant l'interface pour les chargeurs de données.
    
    Cette classe fournit la structure de base pour charger des données dans
    différentes bases de données.

    Attributes:
        connector (DatabaseConnector): Connecteur à la base de données

    Methods:
        clean_column_names(df): Nettoie les noms des colonnes d'un DataFrame
        load_csv(): Charge un fichier CSV dans la base de données
    """

    def __init__(self, connector: DatabaseConnector):
        """
        Initialise le chargeur avec un connecteur de base de données.

        Args:
            connector (DatabaseConnector): Instance d'un connecteur de base de données
        """
        self.connector = connector
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie les noms des colonnes d'un DataFrame.
        
        Cette méthode standardise les noms des colonnes en :
        - Supprimant les espaces en début et fin
        - Remplaçant les espaces par des underscores
        - Remplaçant les tirets par des underscores
        - Convertissant en minuscules

        Args:
            df (pd.DataFrame): DataFrame dont les noms de colonnes doivent être nettoyés

        Returns:
            pd.DataFrame: DataFrame avec les noms de colonnes nettoyés

        Example:
            >>> loader = PostgresLoader(connector)
            >>> df = pd.DataFrame({"Column Name": [1, 2, 3]})
            >>> df = loader.clean_column_names(df)
            >>> print(df.columns)
            ['column_name']
        """
        df.columns = [col.strip().replace(' ', '_').replace('-', '_').lower() 
                     for col in df.columns]
        return df
    
    @abstractmethod
    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000) -> Dict:
        """
        Charge un fichier CSV dans la base de données.
        
        Args:
            chemin_csv (str): Chemin vers le fichier CSV à charger
            nom_table (str): Nom de la table à créer
            separateur (str, optional): Séparateur utilisé dans le fichier CSV
            batch_size (int, optional): Nombre de lignes à insérer par lot

        Returns:
            Dict: Métriques du chargement
                {
                    'table_name': str,      # Nom de la table créée
                    'load_time': float,     # Temps de chargement en secondes
                    'total_rows': int       # Nombre de lignes chargées
                }
        """
        pass

class QueryAnalyzer(ABC):
    """
    Classe abstraite définissant l'interface pour les analyseurs de requêtes.
    
    Cette classe fournit la structure de base pour analyser les performances
    des requêtes SQL sur différentes bases de données.

    Attributes:
        connector (DatabaseConnector): Connecteur à la base de données

    Methods:
        analyze_query(query): Analyse une requête SQL unique
        analyze_multiple_queries(queries): Analyse plusieurs requêtes
        format_metrics(metrics): Formate les métriques de manière uniforme
    """

    def __init__(self, connector: DatabaseConnector):
        """
        Initialise l'analyseur avec un connecteur de base de données.

        Args:
            connector (DatabaseConnector): Instance d'un connecteur de base de données
        """
        self.connector = connector
    
    @abstractmethod
    def analyze_query(self, query: str) -> Dict:
        """
        Analyse une requête SQL et collecte des métriques de performance.
        
        Args:
            query (str): Requête SQL à analyser

        Returns:
            Dict: Métriques de performance
                {
                    'execution_time': float,  # Temps d'exécution en ms
                    'row_count': int,         # Nombre de lignes retournées
                    'physical_reads': int,     # Lectures physiques
                    'physical_writes': int     # Écritures physiques
                }
        """
        pass
    
    def analyze_multiple_queries(self, queries: List[str]) -> List[Dict]:
        """
        Analyse plusieurs requêtes SQL et collecte leurs métriques.
        
        Args:
            queries (List[str]): Liste des requêtes à analyser

        Returns:
            List[Dict]: Liste des métriques pour chaque requête
        """
        results = []
        for i, query in enumerate(queries, 1):
            metrics = self.analyze_query(query)
            if metrics:
                results.append(metrics)
        return results

    def format_metrics(self, metrics: Dict) -> Dict:
        """
        Formate les métriques de manière uniforme.
        
        Args:
            metrics (Dict): Métriques brutes à formater

        Returns:
            Dict: Métriques formatées avec des types cohérents
                {
                    'query': str,              # Requête SQL
                    'execution_time': float,    # Temps en ms
                    'row_count': int,          # Nombre de lignes
                    'physical_reads': int,      # Lectures
                    'physical_writes': int      # Écritures
                }
        """
        return {
            'query': metrics['query'],
            'execution_time': float(metrics['execution_time']),
            'row_count': int(metrics['row_count']),
            'physical_reads': int(metrics.get('physical_reads', 0)),
            'physical_writes': int(metrics.get('physical_writes', 0))
        }