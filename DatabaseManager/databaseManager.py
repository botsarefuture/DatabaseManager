import logging
import os
import sys
from pymongo import MongoClient, errors
from threading import Lock
import importlib.util

# Setup logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None  # Singleton pattern
    _lock = Lock()  # For thread safety

    def __init__(self, config_class=None):
        """
        Initializes the DatabaseManager. A single MongoDB client is used, and databases can be accessed dynamically.

        Parameters
        ----------
        config_class : class, optional
            User can provide their own config class. If None, attempts to load 'Config' from the caller's directory.
        """
        if DatabaseManager._instance is None:
            with DatabaseManager._lock:
                if DatabaseManager._instance is None:
                    self._config = config_class or self._load_config()
                    logger.info("Initializing DatabaseManager instance.")
                    # Load URI and default DB name from Config class
                    self._mongo_uri = self._config.MONGO_URI or 'mongodb://localhost:27017'
                    self._default_db_name = self._config.MONGO_DBNAME or 'testdb'
                    self._client = None
                    self._databases = {}  # Cache for accessed databases
                    self._initialized = False  # Track initialization status
                    DatabaseManager._instance = self  # Save as singleton instance
        else:
            logger.warning("DatabaseManager instance already initialized. Returning existing instance.")

    def _load_config(self):
        """
        Dynamically load the Config class from the appropriate directory based on the caller's location.

        Returns
        -------
        class
            The loaded Config class.
        """
        # Get the caller's directory (the directory from where this class was imported)
        caller_frame = sys._getframe(1)
        caller_file = caller_frame.f_globals.get("__file__", None)
        if not caller_file:
            raise RuntimeError("Unable to locate the calling script's directory.")

        caller_dir = os.path.dirname(os.path.abspath(caller_file))
        own_dir = os.path.dirname(os.path.abspath(__file__))

        if caller_dir == own_dir:
            # Caller is in the same directory as this file
            caller_frame = sys._getframe(2)
            caller_file = caller_frame.f_globals.get("__file__", None)
            if not caller_file:
                raise RuntimeError("Unable to locate the calling script's directory.")

            caller_dir = os.path.dirname(os.path.abspath(caller_file))

        config_path = os.path.join(caller_dir, "config.py")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found in: {os.path.dirname(config_path)}")

        # Import the config module dynamically
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        if not hasattr(config_module, "Config"):
            raise AttributeError(f"'Config' class not found in {config_path}")
        
        return config_module.Config()

    def _init_client(self):
        """
        Initializes MongoDB client connection. This will be reused for accessing multiple databases.

        Raises
        ------
        RuntimeError
            If the MongoDB configuration is missing or connection fails.
        """
        if self._initialized:
            return

        if not self._mongo_uri:
            logger.error("Missing MongoDB configuration: 'MONGO_URI'.")
            raise RuntimeError("Database configuration is missing 'MONGO_URI'.")

        try:
            # Initialize MongoDB client with connection pooling and timeout options
            self._client = MongoClient(
                self._mongo_uri,
                serverSelectionTimeoutMS=5000,  # Connection timeout
                maxPoolSize=50,  # Connection pool size (adjust as needed)
                minPoolSize=5
            )
            # Ping the server to check the connection
            self._client.admin.command("ping")
            self._initialized = True
            logger.info(f"Connected to MongoDB at URI: {self._mongo_uri}")
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB connection timeout: {str(e)}")
            raise RuntimeError(f"Failed to connect to MongoDB: Timeout - {str(e)}")
        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")

    def get_db(self, db_name=None):
        """
        Public method to dynamically switch and get the MongoDB database object.
        Defaults to the initially configured database but allows switching.

        Parameters
        ----------
        db_name : str, optional
            The name of the database. Defaults to the initially configured database.

        Returns
        -------
        Database
            The MongoDB database object.
        """
        if self._client is None:
            logger.info("Initializing MongoDB client.")
            self._init_client()

        # Default to the initially configured database if not specified
        db_name = db_name or self._default_db_name

        if db_name in self._databases:
            logger.info(f"Using cached database connection for: {db_name}")
            return self._databases[db_name]

        # Create and cache the new database connection
        logger.info(f"Switching to database: {db_name}")
        db = self._client[db_name]
        self._databases[db_name] = db  # Cache the database object for future use
        return db

    def list_collections(self, db_name=None):
        """
        Lists all collections in the specified database.

        Parameters
        ----------
        db_name : str, optional
            The name of the database. Defaults to the initially configured database.

        Returns
        -------
        list
            A list of collection names.
        """
        db = self.get_db(db_name)
        return db.list_collection_names()

    def get_collection(self, collection_name, db_name=None):
        """
        Retrieves a specific collection from the specified database.

        Parameters
        ----------
        collection_name : str
            The name of the collection to retrieve.
        db_name : str, optional
            The name of the database. Defaults to the initially configured database.

        Returns
        -------
        Collection
            The MongoDB collection object.
        """
        db = self.get_db(db_name)
        return db[collection_name]

    def close_connection(self):
        """
        Safely closes the MongoDB client connection, ensuring no resources are leaked.
        """
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")
        else:
            logger.warning("Attempted to close a non-existent MongoDB connection.")

    @classmethod
    def get_instance(cls, config_class=None):
        """
        Singleton pattern to ensure only one instance of DatabaseManager is used.
        Optionally allows passing a custom config class.

        Parameters
        ----------
        config_class : class, optional
            User can provide their own config class. If None, attempts to load 'Config' from the caller's directory.

        Returns
        -------
        DatabaseManager
            The singleton instance of DatabaseManager.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = DatabaseManager(config_class)
        return cls._instance

    @staticmethod
    def legacy_get_db():
        """
        Backward-compatible method for retrieving the default database.

        Returns
        -------
        Database
            The MongoDB database object.
        """
        instance = DatabaseManager.get_instance()
        return instance.get_db()
