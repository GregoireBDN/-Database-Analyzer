from ..base_classes import DatabaseLoader
import pandas as pd
import time

class MonetDBLoader(DatabaseLoader):
    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000):
        start_time = time.time()
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        
        
        colonnes = ", ".join([f'"{col}" VARCHAR(255)' for col in df.columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({colonnes})")
        
        valeurs = [tuple(str(x) if pd.notna(x) else None for x in row) 
                  for row in df.values]
        placeholders = ",".join(["%s" for _ in df.columns])
        
        for i in range(0, len(valeurs), batch_size):
            batch = valeurs[i:i + batch_size]
            cursor.executemany(
                f"INSERT INTO {nom_table} VALUES ({placeholders})",
                batch
            )
            conn.commit()
        end_time = time.time()
        total_time = end_time - start_time
        return {
            'table_name': nom_table,
            'load_time': total_time
        }