# DatabaseManager

DatabaseManager is a Python package for managing MongoDB connections with `pymongo`.
It is designed to be predictable: importing and instantiating do not open files or
connect to the database. Configuration and connections are created only when you
call a database method.

## Behavior (No Surprises)

- Importing the package does not read config files or open connections.
- Instantiating `DatabaseManager` does not read config files or open connections.
- Configuration and MongoDB connections are created only when you call `get_db`,
  `get_collection`, or `list_collections`.

## Features

- Lazy config loading and lazy connection setup.
- Singleton instance with thread-safe initialization.
- Auto-discovery of `config.py` with a `Config` class.
- Optional `Config` object with file and environment variable support.
- Database caching for repeated access.
- Clear error handling for missing config or connection failures.

## Requirements

- Python 3.7+
- `pymongo>=3.11`

## Installation

```bash
pip install git+https://github.com/botsarefuture/DatabaseManager.git
```

## Usage

### Option A: Auto-discovered `config.py`

Create a `config.py` in your project directory (the same directory as your app
entry point). The `DatabaseManager` will load it only when the first database
operation is called.

```python
# config.py
class Config:
    MONGO_URI = "mongodb://localhost:27017"
    MONGO_DBNAME = "my_database"
```

```python
from DatabaseManager import DatabaseManager

db_manager = DatabaseManager.get_instance()
db = db_manager.get_db()
```

If `config.py` is missing when a DB call happens, a `FileNotFoundError` is raised.

### Option B: Provide a `Config` object

```python
from DatabaseManager import Config, DatabaseManager

config = Config()
config.MONGO_URI = "mongodb://localhost:27017"
config.MONGO_DBNAME = "custom_database"

db_manager = DatabaseManager.get_instance(config)
db = db_manager.get_db()
```

### Load config from a JSON/YAML/INI file

```python
from DatabaseManager import Config, DatabaseManager

config = Config(config_file="path/to/config.json", config_type="json")
db_manager = DatabaseManager.get_instance(config)
db = db_manager.get_db()
```

### Collections

```python
collection = db_manager.get_collection("users")
document = collection.find_one({"name": "Ada"})
```

### Legacy support

```python
db = DatabaseManager.legacy_get_db()
```

## Environment Variables

`Config` reads environment variables by default:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DBNAME="my_database"
```

## Error Handling

```python
try:
    db_manager = DatabaseManager.get_instance()
    db = db_manager.get_db()
except RuntimeError as exc:
    print(f"Error: {exc}")
```

## Running Tests

```bash
python -m unittest -v DatabaseManager/tests/test_databaseManager.py
```

## Directory Structure

```
DatabaseManager/
├── DatabaseManager/
│   ├── __init__.py
│   ├── databaseManager.py
│   ├── config.py
│   └── tests/
│       └── test_databaseManager.py
├── README.md
└── setup.py
```

## License

MIT
