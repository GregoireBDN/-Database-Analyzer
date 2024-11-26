from ..base_classes import DatabaseLoader
import pandas as pd
import time

class PostgresLoader(DatabaseLoader):
    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000):
        start_time = time.time()
        engine = self.connector.get_connection()
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        
        df.head(0).to_sql(nom_table, engine, if_exists='replace', index=False)
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            batch.to_sql(nom_table, engine, if_exists='append', index=False)
        end_time = time.time()
        total_time = end_time - start_time
        return {
            'table_name': nom_table,
            'load_time': total_time
        }