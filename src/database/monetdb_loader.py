from src.base_classes import DatabaseLoader
import pandas as pd
import time
from tqdm import tqdm

class MonetDBLoader(DatabaseLoader):
    def table_exists(self, nom_table: str) -> bool:
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM sys.tables 
            WHERE name = '{nom_table}' 
            AND system = false
        """)
        return cursor.fetchone()[0] > 0

    def get_row_count(self, nom_table: str) -> int:
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {nom_table}")
        return cursor.fetchone()[0]

    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000):
        print(f"\n📊 MonetDB: Chargement de {nom_table}")
        
        # Vérifier si la table existe déjà
        if self.table_exists(nom_table):
            row_count = self.get_row_count(nom_table)
            print(f"   ℹ️  Table existante ({row_count:,} lignes)")
            return {
                'table_name': nom_table,
                'load_time': 0.001,
                'total_rows': row_count
            }

        start_time = time.time()
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        print("   ├─ Lecture du fichier CSV...")
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        total_rows = len(df)
        
        print(f"   ├─ Création de la table ({len(df.columns)} colonnes)")
        colonnes = ", ".join([f'"{col}" VARCHAR(255)' for col in df.columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nom_table} ({colonnes})")
        
        print(f"   └─ Insertion des données ({total_rows:,} lignes)")
        valeurs = [tuple(str(x) if pd.notna(x) else None for x in row) 
                  for row in df.values]
        placeholders = ",".join(["%s" for _ in df.columns])
        
        # Modification de tqdm pour un affichage plus propre
        with tqdm(total=total_rows, unit='lignes', ncols=80, 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            try:
                for i in range(0, len(valeurs), batch_size):
                    batch = valeurs[i:i + batch_size]
                    cursor.executemany(
                        f"INSERT INTO {nom_table} VALUES ({placeholders})",
                        batch
                    )
                    conn.commit()
                    pbar.update(len(batch))
            except Exception as e:
                print(f"\n   ❌ Erreur lors de l'insertion : {str(e)}")
                return None
        
        end_time = time.time()
        total_time = end_time - start_time
        return {
            'table_name': nom_table,
            'load_time': total_time,
            'total_rows': total_rows
        }