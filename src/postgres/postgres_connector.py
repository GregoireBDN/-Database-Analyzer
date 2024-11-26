import os
from ..base_classes import DatabaseConnector
from sqlalchemy import create_engine

class PostgresConnector(DatabaseConnector):
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