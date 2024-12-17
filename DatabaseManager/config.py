import os
import json
import yaml
import configparser

class Config:
    """
    Configuration class for managing settings.

    Attributes
    ----------
    _mongo_uri : str
        The URI for the MongoDB connection.
    _mongo_dbname : str
        The name of the MongoDB database.

    Methods
    -------
    load_from_env()
        Loads configuration values from environment variables.
    load_from_file(file_path, file_type='json')
        Loads configuration values from a file (JSON, YAML, or INI format).
    update_config(config_dict)
        Updates the configuration values with the provided dictionary.

    Examples
    --------
    >>> config = Config()
    >>> config.MONGO_URI
    'mongodb://localhost:27017'
    >>> config.MONGO_DBNAME
    'testdb'

    Load from environment variables:
    >>> import os
    >>> os.environ['MONGO_URI'] = 'mongodb://example.com:27017'
    >>> os.environ['MONGO_DBNAME'] = 'exampledb'
    >>> config.load_from_env()
    >>> config.MONGO_URI
    'mongodb://example.com:27017'
    >>> config.MONGO_DBNAME
    'exampledb'

    Load from a JSON file:
    >>> config.load_from_file('config.json', 'json')

    Load from a YAML file:
    >>> config.load_from_file('config.yaml', 'yaml')

    Load from an INI file:
    >>> config.load_from_file('config.ini', 'ini')

    Update configuration directly:
    >>> config.update_config({'MONGO_URI': 'mongodb://newhost:27017', 'MONGO_DBNAME': 'newdb'})
    >>> config.MONGO_URI
    'mongodb://newhost:27017'
    >>> config.MONGO_DBNAME
    'newdb'
    """

    def __init__(self, config_file=None, config_type='json'):
        """
        Initializes the configuration. Loads settings from environment variables,
        a provided config file, or defaults.

        Parameters
        ----------
        config_file : str, optional
            Optional file path to load configuration from.
        config_type : str, optional
            Type of configuration file ('json', 'yaml', or 'ini').
        """
        # Default values
        self._mongo_uri = "mongodb://localhost:27017"
        self._mongo_dbname = "testdb"       

        # Load from environment variables if set
        self.load_from_env()

        # Load from config file if provided
        if config_file:
            self.load_from_file(config_file, config_type)

    @property
    def MONGO_URI(self):
        return self._mongo_uri

    @MONGO_URI.setter
    def MONGO_URI(self, value):
        self._mongo_uri = value

    @property
    def MONGO_DBNAME(self):
        return self._mongo_dbname

    @MONGO_DBNAME.setter
    def MONGO_DBNAME(self, value):
        self._mongo_dbname = value
    
    def load_from_env(self):
        """
        Loads configuration values from environment variables, if they exist.
        """
        self._mongo_uri = os.getenv('MONGO_URI', self._mongo_uri)
        self._mongo_dbname = os.getenv('MONGO_DBNAME', self._mongo_dbname)

    def load_from_file(self, file_path, file_type='json'):
        """
        Loads configuration values from a file (JSON, YAML, or INI format).

        Parameters
        ----------
        file_path : str
            The path to the config file.
        file_type : str, optional
            The file format ('json', 'yaml', or 'ini').
        """
        if file_type == 'json':
            self._load_from_json(file_path)
        elif file_type == 'yaml':
            self._load_from_yaml(file_path)
        elif file_type == 'ini':
            self._load_from_ini(file_path)
        else:
            raise ValueError(f"Unsupported config file type: {file_type}")

    def _load_from_json(self, file_path):
        """
        Loads configuration from a JSON file.

        Parameters
        ----------
        file_path : str
            The path to the JSON config file.
        """
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
            self._mongo_uri = config_data.get('MONGO_URI', self._mongo_uri)
            self._mongo_dbname = config_data.get('MONGO_DBNAME', self._mongo_dbname)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def _load_from_yaml(self, file_path):
        """
        Loads configuration from a YAML file.

        Parameters
        ----------
        file_path : str
            The path to the YAML config file.
        """
        try:
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
            self._mongo_uri = config_data.get('MONGO_URI', self._mongo_uri)
            self._mongo_dbname = config_data.get('MONGO_DBNAME', self._mongo_dbname)
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def _load_from_ini(self, file_path):
        """
        Loads configuration from an INI file.

        Parameters
        ----------
        file_path : str
            The path to the INI config file.
        """
        try:
            config = configparser.ConfigParser()
            config.read(file_path)
            self._mongo_uri = config.get('MongoDB', 'MONGO_URI', fallback=self._mongo_uri)
            self._mongo_dbname = config.get('MongoDB', 'MONGO_DBNAME', fallback=self._mongo_dbname)
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def update_config(self, config_dict):
        """
        Updates the configuration values with the provided dictionary.

        Parameters
        ----------
        config_dict : dict
            A dictionary containing configuration values.
        """
        self._mongo_uri = config_dict.get('MONGO_URI', self._mongo_uri)
        self._mongo_dbname = config_dict.get('MONGO_DBNAME', self._mongo_dbname)

    def __repr__(self):
        return f"Config(MONGO_URI={self._mongo_uri}, MONGO_DBNAME={self._mongo_dbname})"
