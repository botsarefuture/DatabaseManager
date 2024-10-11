import os
import json
import yaml
import configparser

class Config:
    """
    A flexible configuration class that can load settings from defaults, 
    environment variables, files (JSON, YAML, or INI), or direct input.
    """

    def __init__(self, config_file=None, config_type='json'):
        """
        Initializes the configuration. Loads settings from environment variables,
        a provided config file, or defaults.

        Args:
        - config_file (str): Optional file path to load configuration from.
        - config_type (str): Type of configuration file ('json', 'yaml', or 'ini').
        """
        # Default values
        self.MONGO_URI = "mongodb://localhost:27017"
        self.MONGO_DBNAME = "testdb"

        # Load from environment variables if set
        self.load_from_env()

        # Load from config file if provided
        if config_file:
            self.load_from_file(config_file, config_type)

    def load_from_env(self):
        """
        Loads configuration values from environment variables, if they exist.
        """
        self.MONGO_URI = os.getenv('MONGO_URI', self.MONGO_URI)
        self.MONGO_DBNAME = os.getenv('MONGO_DBNAME', self.MONGO_DBNAME)

    def load_from_file(self, file_path, file_type='json'):
        """
        Loads configuration values from a file (JSON, YAML, or INI format).

        Args:
        - file_path (str): The path to the config file.
        - file_type (str): The file format ('json', 'yaml', or 'ini').
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

        Args:
        - file_path (str): The path to the JSON config file.
        """
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
            self.MONGO_URI = config_data.get('MONGO_URI', self.MONGO_URI)
            self.MONGO_DBNAME = config_data.get('MONGO_DBNAME', self.MONGO_DBNAME)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def _load_from_yaml(self, file_path):
        """
        Loads configuration from a YAML file.

        Args:
        - file_path (str): The path to the YAML config file.
        """
        try:
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
            self.MONGO_URI = config_data.get('MONGO_URI', self.MONGO_URI)
            self.MONGO_DBNAME = config_data.get('MONGO_DBNAME', self.MONGO_DBNAME)
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def _load_from_ini(self, file_path):
        """
        Loads configuration from an INI file.

        Args:
        - file_path (str): The path to the INI config file.
        """
        try:
            config = configparser.ConfigParser()
            config.read(file_path)
            self.MONGO_URI = config.get('MongoDB', 'MONGO_URI', fallback=self.MONGO_URI)
            self.MONGO_DBNAME = config.get('MongoDB', 'MONGO_DBNAME', fallback=self.MONGO_DBNAME)
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {file_path}: {str(e)}")

    def update_config(self, config_dict):
        """
        Updates the configuration values with the provided dictionary.

        Args:
        - config_dict (dict): A dictionary containing configuration values.
        """
        self.MONGO_URI = config_dict.get('MONGO_URI', self.MONGO_URI)
        self.MONGO_DBNAME = config_dict.get('MONGO_DBNAME', self.MONGO_DBNAME)

    def __repr__(self):
        return f"Config(MONGO_URI={self.MONGO_URI}, MONGO_DBNAME={self.MONGO_DBNAME})"
