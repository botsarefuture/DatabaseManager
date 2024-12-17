# DatabaseManager

**DatabaseManager** is a Python package for managing MongoDB connections with `pymongo`. It offers a simple interface to initialize and access MongoDB databases, making it ideal for quick and efficient database management.

## Features

- **User-Friendly:** Easy MongoDB connection initialization.
- **Configurable:** Load configurations from a file or use a config object.
- **Error Handling:** Catches and raises connection errors.
- **Singleton:** Ensures only one MongoDB connection throughout the application.
- **Environment Support:** Manage sensitive data using environment variables.
- **Thread-Safe:** Uses a lock for thread-safe singleton initialization.
- **Dynamic Config Loading:** Automatically loads `Config` class from the project directory.
- **Database Caching:** Caches databases for better performance.

## Requirements

- **Python:** 3.7+
- **Dependencies:** `pymongo>=3.11`

## Installation

Install **DatabaseManager** directly from GitHub:

```bash
pip install git+https://github.com/botsarefuture/DatabaseManager.git
```

## Usage

### Configuration Setup

Configure MongoDB settings using the built-in `Config` class. The `DatabaseManager` will automatically attempt to load a `config.py` containing a `Config` class from your project directory.

#### Example Configuration (`config.py`):

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'your_database_name'

    def load_from_json(self, filepath):
        import json
        with open(filepath, 'r') as file:
            config_data = json.load(file)
        self.MONGO_URI = config_data.get('MONGO_URI', self.MONGO_URI)
        self.MONGO_DBNAME = config_data.get('MONGO_DBNAME', self.MONGO_DBNAME)
        return self
```

#### Using the `Config` Class:

```python
from DatabaseManager import Config, DatabaseManager

config = Config().load_from_json("path/to/config.json")
db_manager = DatabaseManager(config).get_instance()
db = db_manager.get_db()

collection = db['your_collection']
document = collection.find_one({"key": "value"})
print(document)
```

### Manual Configuration

You can also manually configure the `DatabaseManager`:

```python
from DatabaseManager import DatabaseManager

db_manager = DatabaseManager().get_instance()
db_manager._mongo_uri = 'mongodb://localhost:27017'
db_manager._mongo_default_dbname = 'your_database_name'

db = db_manager.get_db()
```

> **Note:** Changing the configuration manually will affect all instances. Using the `Config` class is recommended for custom configurations.

### Default Configuration

If no custom configuration is provided, **DatabaseManager** defaults to:

- **`MONGO_URI`:** `'mongodb://localhost:27017'`
- **`MONGO_DBNAME`:** `'testdb'`

You can also pass a custom `Config` object directly:

```python
from DatabaseManager import Config, DatabaseManager

config = Config()
config.MONGO_URI = 'mongodb://localhost:27017'
config.MONGO_DBNAME = 'custom_database'

db_manager = DatabaseManager(config).get_instance()
```

### Error Handling

Errors during connection initialization will be raised:

```python
try:
    db_manager = DatabaseManager(config).get_instance()
    db = db_manager.get_db()
except RuntimeError as e:
    print(f"Error: {e}")
```

## Configuration Details

### `Config` Class

The `Config` class manages MongoDB settings, supporting loading from a JSON file or manual configuration.

#### Example `Config` Class:

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'my_database'

    def load_from_json(self, filepath):
        import json
        with open(filepath, 'r') as file:
            config_data = json.load(file)
        self.MONGO_URI = config_data.get('MONGO_URI', self.MONGO_URI)
        self.MONGO_DBNAME = config_data.get('MONGO_DBNAME', self.MONGO_DBNAME)
        return self
```

#### Using Environment Variables (Optional)

For added security, use environment variables for sensitive data:

```python
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'my_database')
```

Set environment variables:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DBNAME="my_database"
```

### Legacy Support

For backward compatibility, use the `legacy_get_db()` method to retrieve the default database without a config object:

```python
db = DatabaseManager.legacy_get_db()
```

## Directory Structure

```
DatabaseManager/
│
├── DatabaseManager/
│   ├── __init__.py           # Package initialization
│   ├── databaseManager.py    # DatabaseManager class
│   ├── config.py             # Config class
│
├── setup.py                  # Package setup
├── README.md                 # Documentation
├── requirements.txt          # Dependencies
```

## Contributing

1. **Fork the repository.**
2. **Create a branch:** `git checkout -b my-new-feature`
3. **Commit your changes:** `git commit -am 'Add feature'`
4. **Push to the branch:** `git push origin my-new-feature`
5. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.