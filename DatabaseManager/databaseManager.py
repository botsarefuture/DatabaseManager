import logging
import os
import sys
from pymongo import MongoClient, errors
from threading import Lock
import importlib.util

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    A singleton class for managing MongoDB connections and database access dynamically.

    Attributes
    ----------
    _instance : DatabaseManager or None
        Singleton instance of the DatabaseManager.
    _lock : threading.Lock
        Lock to ensure thread-safe singleton initialization.
    _config : class
        Config class containing MongoDB configuration.
    _mongo_uri : str
        MongoDB URI obtained from the Config class.
    _default_db_name : str
        Default database name to connect to.
    _client : pymongo.MongoClient
        MongoDB client instance.
    _databases : dict
        Cache of accessed databases for optimized performance.
    _initialized : bool
        Indicates if the MongoDB client has been initialized.

    Methods
    -------
    __init__(config_class=None)
        Initializes the DatabaseManager singleton instance.
    _load_config()
        Dynamically loads the Config class from the caller's directory.
    _init_client()
        Initializes the MongoDB client connection.
    get_db(db_name=None)
        Returns a MongoDB database instance.
    list_collections(db_name=None)
        Lists all collections in the specified database.
    get_collection(collection_name, db_name=None)
        Retrieves a specific collection from the database.
    close_connection()
        Closes the MongoDB client connection.
    get_instance(config_class=None)
        Returns the singleton instance of the DatabaseManager.
    """

    _instance = None
    _lock = Lock()

    def __init__(self, config_class=None):
        """
        Initialize the DatabaseManager singleton.

        Parameters
        ----------
        config_class : class, optional
            Config class containing MongoDB configuration.
            If None, the class attempts to dynamically load 'Config'.
        """
        if DatabaseManager._instance is None:
            with DatabaseManager._lock:
                if DatabaseManager._instance is None:
                    self._config = config_class or self._load_config()
                    logger.info("Initializing DatabaseManager instance.")
                    self._mongo_uri = self._config.MONGO_URI or "mongodb://localhost:27017"
                    self._default_db_name = self._config.MONGO_DBNAME or "testdb"
                    self._client = None
                    self._databases = {}
                    self._initialized = False
                    DatabaseManager._instance = self
        else:
            logger.warning("DatabaseManager instance already initialized.")

    def _load_config(self):
        """
        Dynamically load the Config class from the calling script's directory.

        Returns
        -------
        class
            Loaded Config class.

        Raises
        ------
        RuntimeError
            If the calling script's directory cannot be located.
        FileNotFoundError
            If 'config.py' is missing.
        AttributeError
            If 'Config' class is not found in 'config.py'.
        """
        caller_frame = sys._getframe(1)
        caller_file = caller_frame.f_globals.get("__file__")
        if not caller_file:
            raise RuntimeError("Unable to determine the caller's script location.")

        caller_dir = os.path.dirname(os.path.abspath(caller_file))
        own_dir = os.path.dirname(os.path.abspath(__file__))
        if caller_dir == own_dir:
            caller_frame = sys._getframe(2)
            caller_file = caller_frame.f_globals.get("__file__")
            if not caller_file:
                raise RuntimeError("Unable to determine the caller's script location.")

            caller_dir = os.path.dirname(os.path.abspath(caller_file))
                                                         
        config_path = os.path.join(caller_dir, "config.py")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        if not hasattr(config_module, "Config"):
            raise AttributeError("Config class not found in 'config.py'.")

        return config_module.Config()

    def _init_client(self):
        """
        Initialize the MongoDB client.

        Raises
        ------
        RuntimeError
            If MongoDB URI is missing or connection fails.
        """
        if self._initialized:
            return

        if not self._mongo_uri:
            raise RuntimeError("MongoDB configuration 'MONGO_URI' is missing.")

        try:
            self._client = MongoClient(
                self._mongo_uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=5,
            )
            self._client.admin.command("ping")
            self._initialized = True
            logger.info(f"Connected to MongoDB: {self._mongo_uri}")
        except errors.ServerSelectionTimeoutError as exc:
            raise RuntimeError(f"MongoDB connection timeout: {exc}")
        except Exception as exc:
            raise RuntimeError(f"MongoDB connection error: {exc}")

    def get_db(self, db_name=None):
        """
        Retrieve a MongoDB database instance.

        Parameters
        ----------
        db_name : str, optional
            Name of the database. Defaults to the configured default database name.

        Returns
        -------
        Database
            MongoDB database object.
        """
        if self._client is None:
            self._init_client()

        db_name = db_name or self._default_db_name
        if db_name not in self._databases:
            self._databases[db_name] = self._client[db_name]
            logger.info(f"Connected to database: {db_name}")
        return self._databases[db_name]

    def list_collections(self, db_name=None):
        """
        List all collections in the specified database.

        Parameters
        ----------
        db_name : str, optional
            Name of the database. Defaults to the configured default database.

        Returns
        -------
        list of str
            List of collection names in the database.
        """
        db = self.get_db(db_name)
        return db.list_collection_names()

    def get_collection(self, collection_name, db_name=None):
        """
        Retrieve a specific collection from the database.

        Parameters
        ----------
        collection_name : str
            Name of the collection to retrieve.
        db_name : str, optional
            Name of the database. Defaults to the configured default database.

        Returns
        -------
        Collection
            MongoDB collection object.
        """
        db = self.get_db(db_name)
        return db[collection_name]

    def close_connection(self):
        """
        Close the MongoDB client connection.

        Returns
        -------
        None
        """
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")
            self._initialized = False

    @staticmethod
    def get_instance(config_class=None):
        """
        Get the singleton instance of the DatabaseManager.

        Parameters
        ----------
        config_class : class, optional
            Config class containing MongoDB configuration.

        Returns
        -------
        DatabaseManager
            Singleton instance of the DatabaseManager.
        """
        if DatabaseManager._instance is None:
            DatabaseManager(config_class)
        return DatabaseManager._instance