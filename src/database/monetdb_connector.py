from src.base_classes import DatabaseConnector
import pymonetdb
import os

class MonetDBConnector(DatabaseConnector):
    """
    Connecteur pour la base de données MonetDB.
    
    Cette classe gère la connexion à une instance MonetDB en utilisant les variables
    d'environnement pour la configuration. Elle hérite de DatabaseConnector et
    implémente les méthodes spécifiques à MonetDB.

    Attributes:
        user (str): Nom d'utilisateur MonetDB (défaut: 'monetdb')
        password (str): Mot de passe MonetDB (défaut: 'monetdb')
        host (str): Hôte MonetDB (défaut: 'localhost')
        database (str): Nom de la base de données (défaut: 'databaseAnnalizationProject')
        port (int): Port MonetDB (défaut: 50000)
        connection: Objet de connexion MonetDB (initialisé à None)

    Notes:
        Les paramètres de connexion peuvent être configurés via les variables
        d'environnement suivantes :
        - MONETDB_USER
        - MONETDB_PASSWORD
        - MONETDB_HOST
        - MONETDB_DB
        - MONETDB_PORT
    """

    def _load_env_vars(self):
        """
        Charge les paramètres de connexion depuis les variables d'environnement.
        
        Cette méthode initialise les attributs de connexion en utilisant les variables
        d'environnement si elles sont définies, sinon utilise les valeurs par défaut.
        """
        self.user = os.getenv('MONETDB_USER', 'monetdb')
        self.password = os.getenv('MONETDB_PASSWORD', 'monetdb')
        self.host = os.getenv('MONETDB_HOST', 'localhost')
        self.database = os.getenv('MONETDB_DB', 'databaseAnnalizationProject')
        self.port = int(os.getenv('MONETDB_PORT', 50000))
    
    def connect(self):
        """
        Établit une connexion à la base de données MonetDB.
        
        Returns:
            pymonetdb.Connection: Objet de connexion MonetDB
            
        Notes:
            La connexion n'est établie que si elle n'existe pas déjà.
            Les paramètres de connexion sont chargés depuis les variables d'environnement.
        """
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
        """
        Récupère la connexion existante ou en crée une nouvelle.
        
        Returns:
            pymonetdb.Connection: Objet de connexion MonetDB actif
            
        Notes:
            Cette méthode assure qu'une connexion active est toujours disponible.
        """
        if not self.connection:
            self.connect()
        return self.connection