from ..base_classes import QueryAnalyzer
import time
from typing import Dict
class MonetDBAnalyzer(QueryAnalyzer):
    def analyze_query(self, query: str) -> Dict:
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchall()
        execution_time = (time.time() - start_time) * 1000
        
        cursor.execute("SELECT * FROM sys.storage()")
        storage_stats = cursor.fetchall()
        
        return {
            'execution_time': execution_time,
            'row_count': len(result),
            'physical_reads': sum(row[3] for row in storage_stats),
            'physical_writes': sum(row[4] for row in storage_stats)
        }