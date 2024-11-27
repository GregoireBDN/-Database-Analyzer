from src.base_classes import DatabaseLoader
import pandas as pd
import time
from tqdm import tqdm

class PostgresLoader(DatabaseLoader):
    def table_exists(self, nom_table: str) -> bool:
        engine = self.connector.get_connection()
        query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{nom_table}'
            );
        """
        return pd.read_sql_query(query, engine).iloc[0, 0]

    def get_row_count(self, nom_table: str) -> int:
        engine = self.connector.get_connection()
        query = f"SELECT COUNT(*) FROM {nom_table}"
        return pd.read_sql_query(query, engine).iloc[0, 0]

    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000):
        print(f"\n🐘 PostgreSQL: Chargement de {nom_table}")
        
        # Vérifier si la table existe déjà
        if self.table_exists(nom_table):
            row_count = self.get_row_count(nom_table)
            print(f"   ℹ️  Table existante ({row_count:,} lignes)")
            return {
                'table_name': nom_table,
                'load_time': 0,
                'total_rows': row_count
            }

        start_time = time.time()
        engine = self.connector.get_connection()
        
        print("   ├─ Lecture du fichier CSV...")
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        total_rows = len(df)
        
        print(f"   ├─ Création de la table ({len(df.columns)} colonnes)")
        df.head(0).to_sql(nom_table, engine, if_exists='replace', index=False)
        
        print(f"   └─ Insertion des données ({total_rows:,} lignes)")
        with tqdm(total=total_rows, unit='lignes', ncols=80) as pbar:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i + batch_size]
                batch.to_sql(nom_table, engine, if_exists='append', index=False)
                pbar.update(len(batch))
        
        end_time = time.time()
        total_time = end_time - start_time
        return {
            'table_name': nom_table,
            'load_time': total_time,
            'total_rows': total_rows
        }