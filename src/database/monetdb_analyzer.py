from src.base_classes import QueryAnalyzer
import time
from typing import Dict

class MonetDBAnalyzer(QueryAnalyzer):
    def analyze_query(self, query: str) -> Dict:
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        # Exécution de la requête
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchall()
        execution_time = (time.time() - start_time) * 1000
        
        # Récupération des statistiques de stockage
        try:
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(count), 0) as total_reads
                FROM sys.statistics
                WHERE "schema" NOT IN ('tmp', 'sys')
            """)
            stats = cursor.fetchone()
            physical_reads = int(stats[0]) if stats else 0
            physical_writes = 0
        except Exception as e:
            physical_reads = 0
            physical_writes = 0
            print(f"⚠️  Impossible de récupérer les statistiques de stockage MonetDB: {str(e)}")
        
        return {
            'execution_time': execution_time,
            'row_count': len(result),
            'physical_reads': physical_reads,
            'physical_writes': physical_writes
        }