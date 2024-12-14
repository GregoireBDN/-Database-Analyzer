"""
Analyseur de performances pour PostgreSQL.

Ce module fournit une implémentation concrète de QueryAnalyzer pour PostgreSQL,
permettant d'analyser les performances des requêtes SQL en utilisant EXPLAIN ANALYZE.
"""

from src.base_classes import QueryAnalyzer
from sqlalchemy import text
from typing import Dict
import time

class PostgresAnalyzer(QueryAnalyzer):
    """
    Analyseur de performances pour les requêtes PostgreSQL.
    
    Cette classe utilise la commande EXPLAIN ANALYZE de PostgreSQL pour collecter
    des métriques détaillées sur l'exécution des requêtes, incluant les temps
    d'exécution et les statistiques d'accès aux données.

    Attributes:
        connector: Instance de PostgresConnector pour la connexion à la base

    Notes:
        Les métriques collectées incluent :
        - Temps d'exécution total (planification + exécution)
        - Nombre de lignes retournées
        - Nombre de lectures physiques
        - Nombre d'écritures physiques
    """

    def analyze_query(self, query: str) -> Dict:
        """
        Analyse une requête SQL et mesure son temps d'exécution.
        
        Args:
            query (str): Requête SQL à analyser

        Returns:
            Dict: Métriques de performance
                {
                    'execution_time': float,  # Temps total en ms
                    'row_count': int,         # Nombre de lignes retournées
                    'physical_reads': int,     # Toujours 0 (pour uniformité)
                    'physical_writes': int     # Toujours 0 (pour uniformité)
                }
        """
        engine = self.connector.get_connection()
        
        with engine.connect() as conn:
            # Mesure directe du temps d'exécution
            start_time = time.time()
            result = conn.execute(text(query))
            rows = result.fetchall()
            execution_time = (time.time() - start_time) * 1000  # Conversion en ms
            
            return {
                'execution_time': execution_time,
                'row_count': len(rows),
                'physical_reads': 0,  # Valeurs uniformisées avec MonetDB
                'physical_writes': 0
            }

    def format_metrics(self, metrics: Dict) -> Dict:
        """
        Formate les métriques brutes en un format standardisé.
        
        Cette méthode assure que toutes les métriques sont dans un format
        cohérent et utilisable pour la génération de rapports.

        Args:
            metrics (Dict): Métriques brutes de l'analyse

        Returns:
            Dict: Métriques formatées
                {
                    'execution_time': float,  # Temps en ms
                    'row_count': int,         # Nombre de lignes
                    'physical_reads': int,     # Lectures
                    'physical_writes': int     # Écritures
                }

        Example:
            >>> raw_metrics = analyzer.analyze_query(query)
            >>> formatted = analyzer.format_metrics(raw_metrics)
            >>> print(formatted['execution_time'])
        """
        return {
            'execution_time': float(metrics['execution_time']),
            'row_count': int(metrics['row_count']),
            'physical_reads': int(metrics.get('physical_reads', 0)),
            'physical_writes': int(metrics.get('physical_writes', 0))
        }