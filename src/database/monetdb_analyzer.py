from src.base_classes import QueryAnalyzer
import time
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class MonetDBAnalyzer(QueryAnalyzer):
    """
    Analyseur de performances pour les requêtes MonetDB.
    
    Cette classe mesure les temps d'exécution des requêtes sur MonetDB et collecte
    des métriques de performance basiques. Contrairement à PostgreSQL, MonetDB
    ne fournit pas nativement des statistiques détaillées sur l'utilisation
    des ressources.

    Attributes:
        connector: Instance de MonetDBConnector pour la connexion à la base

    Notes:
        Les métriques collectées incluent :
        - Temps d'exécution total
        - Nombre de lignes retournées
        - Les lectures/écritures physiques ne sont pas disponibles dans MonetDB
          et sont donc toujours à 0 pour maintenir une uniformité avec PostgreSQL
    """

    def analyze_query(self, query: str) -> Dict:
        """
        Analyse une requête SQL et mesure son temps d'exécution sur MonetDB.
        
        Cette méthode exécute la requête dans une transaction isolée et mesure
        le temps total d'exécution. En cas d'erreur, la transaction est annulée
        et l'erreur est journalisée.
        
        Args:
            query (str): Requête SQL à analyser

        Returns:
            Dict: Métriques de performance
                {
                    'execution_time': float,  # Temps total en ms
                    'row_count': int,         # Nombre de lignes retournées
                    'physical_reads': int,     # Toujours 0 (non disponible)
                    'physical_writes': int     # Toujours 0 (non disponible)
                }
                
                En cas d'erreur :
                {
                    'error': str  # Message d'erreur
                }
        """
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        try:
            # S'assurer qu'il n'y a pas de transaction en cours
            conn.rollback()
            
            # Exécution de la requête avec mesure du temps
            start_time = time.time()
            cursor.execute(query)
            result = cursor.fetchall() if cursor.description else []
            execution_time = (time.time() - start_time) * 1000
            conn.commit()
            
            return {
                'execution_time': execution_time,
                'row_count': len(result),
                'physical_reads': 0,  # Valeurs par défaut car non disponibles
                'physical_writes': 0  # Valeurs par défaut car non disponibles
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la requête: {str(e)}")
            conn.rollback()
            return {'error': str(e)}