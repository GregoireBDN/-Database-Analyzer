"""
Connecteur pour la base de données PostgreSQL.

Ce module fournit une implémentation concrète de DatabaseConnector
pour PostgreSQL, gérant la connexion et la configuration de la base
de données à partir des variables d'environnement.
"""

import os
from src.base_classes import DatabaseConnector
from sqlalchemy import create_engine

class PostgresConnector(DatabaseConnector):
    """
    Implémentation du connecteur PostgreSQL.
    
    Cette classe gère la connexion à une base de données PostgreSQL en utilisant
    SQLAlchemy comme moteur de connexion. Elle charge sa configuration depuis
    les variables d'environnement.

    Attributes:
        user (str): Nom d'utilisateur PostgreSQL
        password (str): Mot de passe PostgreSQL
        host (str): Hôte du serveur PostgreSQL
        database (str): Nom de la base de données
        port (int): Port de connexion PostgreSQL
        connection: Objet SQLAlchemy Engine

    Environment Variables:
        POSTGRES_USER: Nom d'utilisateur (défaut: 'postgres')
        POSTGRES_PASSWORD: Mot de passe (défaut: 'postgres')
        POSTGRES_HOST: Hôte (défaut: 'localhost')
        POSTGRES_DB: Nom de la base de données (défaut: 'databaseAnnalizationProject')
        POSTGRES_PORT: Port (défaut: 5433)
    """
    def _load_env_vars(self):
        self.user = os.getenv('POSTGRES_USER', 'postgres')
        self.password = os.getenv('POSTGRES_PASSWORD', 'postgres')
        self.host = os.getenv('POSTGRES_HOST', 'localhost')
        self.database = os.getenv('POSTGRES_DB', 'databaseAnnalizationProject')
        self.port = int(os.getenv('POSTGRES_PORT', 5433))
    
    def connect(self):
        if not self.connection:
            self.connection = create_engine(
                f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
        return self.connection
    
    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection