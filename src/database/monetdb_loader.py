from src.base_classes import DatabaseLoader
import pandas as pd
import time
from tqdm import tqdm
import numpy as np

"""
Chargeur de données pour MonetDB.

Ce module fournit une implémentation concrète de DatabaseLoader pour MonetDB,
permettant le chargement et la gestion des données depuis des fichiers CSV.
"""

class MonetDBLoader(DatabaseLoader):
    """
    Chargeur de données pour MonetDB. Gère le chargement des fichiers CSV dans la base de données.

    Cette classe hérite de DatabaseLoader et implémente les méthodes spécifiques à MonetDB
    pour le chargement et la vérification des données.

    Attributes:
        connector: Instance de MonetDBConnector pour la connexion à la base de données

    Methods:
        table_exists(nom_table: str) -> bool:
            Vérifie si une table existe dans la base de données.

        get_row_count(nom_table: str) -> int:
            Retourne le nombre de lignes dans une table.

        load_csv(chemin_csv: str, nom_table: str, separateur: str = ',', batch_size: int = 1000) -> dict:
            Charge un fichier CSV dans une table MonetDB.
    """

    def table_exists(self, nom_table: str) -> bool:
        """
        Vérifie si une table existe dans la base de données MonetDB.

        Args:
            nom_table (str): Nom de la table à vérifier

        Returns:
            bool: True si la table existe, False sinon

        Example:
            >>> loader = MonetDBLoader(connector)
            >>> exists = loader.table_exists("air_quality")
            >>> print(f"La table existe: {exists}")
        """
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM sys.tables 
            WHERE name = %s 
            AND system = false
        """, (nom_table,))
        return cursor.fetchone()[0] > 0

    def get_row_count(self, nom_table: str) -> int:
        """
        Retourne le nombre de lignes dans une table MonetDB.

        Args:
            nom_table (str): Nom de la table dont on veut compter les lignes

        Returns:
            int: Nombre de lignes dans la table

        Example:
            >>> loader = MonetDBLoader(connector)
            >>> count = loader.get_row_count("air_quality")
            >>> print(f"Nombre de lignes: {count}")
        """
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {nom_table}")
        return cursor.fetchone()[0]

    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', batch_size: int = 1000) -> dict:
        """
        Charge un fichier CSV dans une table MonetDB.
        """
        print(f"\n📊 MonetDB: Chargement de {nom_table}")
        
        conn = self.connector.get_connection()
        cursor = conn.cursor()
        
        start_time = time.time()
        
        print("   ├─ Vérification de la table existante...")
        if self.table_exists(nom_table):
            cursor.execute(f"DROP TABLE IF EXISTS {nom_table}")
        
        print("   ├─ Lecture du fichier CSV...")
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        df = df.replace({pd.NA: None, np.nan: None})
        total_rows = len(df)
        
        print(f"   ├─ Création de la table ({len(df.columns)} colonnes)")
        
        # Création de la table avec les types appropriés
        columns = []
        for col in df.columns:
            dtype = df[col].dtype
            if dtype == 'int64':
                sql_type = 'BIGINT'
            elif dtype == 'float64':
                sql_type = 'DOUBLE PRECISION'
            else:
                sql_type = 'VARCHAR(1024)'
            columns.append(f'"{col}" {sql_type}')
        
        create_table_sql = f'CREATE TABLE "{nom_table}" ({", ".join(columns)})'
        cursor.execute(create_table_sql)
        
        print(f"   └─ Insertion des données ({total_rows:,} lignes)", end='\r')
        with tqdm(total=total_rows, unit='lignes', ncols=80) as pbar:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i + batch_size]
                
                # Préparation des valeurs pour l'insertion
                placeholders = ','.join(['%s' for _ in range(len(df.columns))])
                column_names = '","'.join(df.columns)
                insert_sql = f'INSERT INTO "{nom_table}" ("{column_names}") VALUES ({placeholders})'
                
                # Conversion des données en liste de tuples
                data = [tuple(x) for x in batch.values]
                
                # Exécution de l'insertion
                cursor.executemany(insert_sql, data)
                pbar.update(len(batch))
        
        print(f"\r      ✓ {total_rows:,} lignes insérées")
        
        conn.commit()
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            'table_name': nom_table,
            'load_time': total_time,
            'total_rows': total_rows
        }