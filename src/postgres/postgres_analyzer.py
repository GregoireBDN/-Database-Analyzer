from ..base_classes import QueryAnalyzer
from sqlalchemy import text
from typing import Dict

class PostgresAnalyzer(QueryAnalyzer):
    def analyze_query(self, query: str) -> Dict:
        engine = self.connector.get_connection()
        explain_query = f"EXPLAIN (FORMAT JSON, ANALYZE, BUFFERS) {query}"
        
        with engine.connect() as conn:
            result = conn.execute(text(explain_query))
            plan = result.fetchall()[0][0][0]
            
            return {
                'execution_time': plan['Execution Time'] + plan['Planning Time'],
                'row_count': plan['Plan']['Actual Rows'],
                'physical_reads': plan['Plan'].get('Shared Read Blocks', 0),
                'physical_writes': plan['Plan'].get('Shared Written Blocks', 0)
            }