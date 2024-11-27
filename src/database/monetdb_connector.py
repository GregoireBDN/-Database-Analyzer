from src.base_classes import DatabaseConnector
import pymonetdb
import os

class MonetDBConnector(DatabaseConnector):
    def _load_env_vars(self):
        self.user = os.getenv('MONETDB_USER', 'monetdb')
        self.password = os.getenv('MONETDB_PASSWORD', 'monetdb')
        self.host = os.getenv('MONETDB_HOST', 'localhost')
        self.database = os.getenv('MONETDB_DB', 'databaseAnnalizationProject')
        self.port = int(os.getenv('MONETDB_PORT', 50000))
    
    def connect(self):
        if not self.connection:
            self.connection = pymonetdb.connect(
                username=self.user,
                password=self.password,
                hostname=self.host,
                database=self.database,
                port=self.port
            )
        return self.connection
    
    def get_connection(self):
        return self.connect()