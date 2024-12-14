from src.base_classes import DatabaseLoader
import pandas as pd
import time
from tqdm import tqdm
from sqlalchemy import text

class PostgresLoader(DatabaseLoader):
    """
    Chargeur de données pour PostgreSQL. Gère le chargement des fichiers CSV dans la base de données.

    Cette classe hérite de DatabaseLoader et implémente les méthodes spécifiques à PostgreSQL
    pour le chargement et la vérification des données.

    Attributes:
        connector: Instance de PostgresConnector pour la connexion à la base de données

    Methods:
        table_exists(nom_table: str) -> bool:
            Vérifie si une table existe dans la base de données.

        get_row_count(nom_table: str) -> int:
            Retourne le nombre de lignes dans une table.

        load_csv(chemin_csv: str, nom_table: str, separateur: str = ',', batch_size: int = 1000) -> dict:
            Charge un fichier CSV dans une table PostgreSQL.
    """

    def table_exists(self, nom_table: str) -> bool:
        """
        Vérifie si une table existe dans la base de données PostgreSQL.

        Args:
            nom_table (str): Nom de la table à vérifier

        Returns:
            bool: True si la table existe, False sinon

        Example:
            >>> loader = PostgresLoader(connector)
            >>> exists = loader.table_exists("air_quality")
            >>> print(f"La table existe: {exists}")
        """
        engine = self.connector.get_connection()
        query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{nom_table}'
            );
        """
        return pd.read_sql_query(query, engine).iloc[0, 0]

    def get_row_count(self, nom_table: str) -> int:
        """
        Retourne le nombre de lignes dans une table PostgreSQL.

        Args:
            nom_table (str): Nom de la table dont on veut compter les lignes

        Returns:
            int: Nombre de lignes dans la table

        Example:
            >>> loader = PostgresLoader(connector)
            >>> count = loader.get_row_count("air_quality")
            >>> print(f"Nombre de lignes: {count}")
        """
        engine = self.connector.get_connection()
        query = f"SELECT COUNT(*) FROM {nom_table}"
        return pd.read_sql_query(query, engine).iloc[0, 0]

    def load_csv(self, chemin_csv: str, nom_table: str, separateur: str = ',', 
                 batch_size: int = 1000) -> dict:
        """
        Charge un fichier CSV dans une table PostgreSQL.
        """
        print(f"\n🐘 PostgreSQL: Chargement de {nom_table}")
        
        engine = self.connector.get_connection()
        start_time = time.time()
        
        print("   ├─ Vérification de la table existante...")
        if self.table_exists(nom_table):
            with engine.connect() as connection:
                connection.execute(text(f"DROP TABLE IF EXISTS {nom_table} CASCADE"))
        
        print("   ├─ Lecture du fichier CSV...")
        df = pd.read_csv(chemin_csv, sep=separateur)
        df = self.clean_column_names(df)
        total_rows = len(df)
        
        print(f"   ├─ Création de la table ({len(df.columns)} colonnes)")
        df.head(0).to_sql(nom_table, engine, if_exists='replace', index=False)
        
        print(f"   └─ Insertion des données ({total_rows:,} lignes)", end='\r')
        with tqdm(total=total_rows, unit='lignes', ncols=80) as pbar:
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i + batch_size]
                batch.to_sql(nom_table, engine, if_exists='append', index=False)
                pbar.update(len(batch))
        
        print(f"\r      ✓ {total_rows:,} lignes insérées")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            'table_name': nom_table,
            'load_time': total_time,
            'total_rows': total_rows
        }