# DatabaseManager

**DatabaseManager** is a Python package for managing MongoDB connections using `pymongo`. It provides an easy-to-use interface to initialize and access MongoDB databases with minimal setup, making it perfect for developers who want a quick and efficient way to manage their database connections.

## Features

- **User-Friendly:** Simplifies MongoDB connection initialization with a clear interface.
- **Configurable:** Easily manage configurations by loading from a file or passing a config object directly.
- **Robust Error Handling:** Catches and raises errors for failed or misconfigured connections.
- **Singleton Pattern:** Ensures only one MongoDB connection is used throughout the application.
- **Environment Variable Support:** Allows sensitive data management using environment variables.

## Requirements

- **Python:** 3.7+
- **Dependencies:** `pymongo`

## Installation

1. **Clone the Repository:**

   Start by cloning the repository or downloading it directly:

   ```bash
   git clone https://github.com/botsarefuture/DatabaseManager.git
   cd DatabaseManager
   ```

2. **Install the Package:**

   Use `pip` to install the package and its dependencies:

   ```bash
   pip install .
   ```

3. **Install from PyPI (Optional):**

   If the package is available on PyPI, you can install it directly using:

   ```bash
   pip install DatabaseManager
   ```

## Usage

### Configuration Setup

You can configure your MongoDB settings using the built-in `Config` class. The `Config` class allows loading your settings from a JSON file or passing them directly.

#### Example Configuration File (`config.json`):

```json
{
    "MONGO_URI": "mongodb://localhost:27017",
    "MONGO_DBNAME": "your_database_name"
}
```

#### Using the `Config` Class

Here's how you can load your configuration and initialize the **DatabaseManager** with the custom configuration:

```python
from DatabaseManager import Config, DatabaseManager

# Load configuration from a JSON file
config = Config().load_from_json("path/to/your/config.json")

# Initialize the DatabaseManager with the custom config
db_manager = DatabaseManager(config)

# Retrieve the MongoDB database instance
db = db_manager.get_db()

# Interact with your MongoDB collections
collection = db['your_collection_name']
document = collection.find_one({"key": "value"})
print(document)
```

### Default Configuration

If no custom configuration is provided, the **DatabaseManager** will default to the following values:

- **`MONGO_URI`:** `'mongodb://localhost:27017'`
- **`MONGO_DBNAME`:** `'testdb'`

You can also pass a custom `Config` object directly if you prefer not to use JSON files:

```python
from DatabaseManager import Config, DatabaseManager

# Define configuration in Python
config = Config()
config.MONGO_URI = 'mongodb://localhost:27017'
config.MONGO_DBNAME = 'custom_database'

# Initialize the DatabaseManager with the custom config
db_manager = DatabaseManager(config)
```

### Error Handling

The package includes error handling for connection issues. If the database connection fails or is misconfigured, an appropriate error will be raised:

```python
try:
    db_manager = DatabaseManager(config)
    db = db_manager.get_db()
except RuntimeError as e:
    print(f"Error: {e}")
```

## Configuration Details

### `Config` Class

The `Config` class handles the MongoDB connection settings. It supports loading from a JSON file or manually setting attributes.

#### Example Config Class:

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

#### Environment Variables (Optional)

For enhanced security, you can use environment variables to manage sensitive data. Here's an example of modifying the `Config` class to read from environment variables:

```python
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'my_database')

    def load_from_json(self, filepath):
        import json
        with open(filepath, 'r') as file:
            config_data = json.load(file)
        self.MONGO_URI = config_data.get('MONGO_URI', self.MONGO_URI)
        self.MONGO_DBNAME = config_data.get('MONGO_DBNAME', self.MONGO_DBNAME)
        return self
```

Set your environment variables like this:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DBNAME="my_database"
```

### Legacy Support

For backward compatibility, the package supports a `legacy_get_db()` method that allows you to retrieve the default database without specifying a config object:

```python
db = DatabaseManager.legacy_get_db()
```

## Directory Structure

Here’s how the package is organized:

```
DatabaseManager/
│
├── DatabaseManager/
│   ├── __init__.py           # Package initialization
│   ├── databaseManager.py    # The DatabaseManager class
│   ├── config.py             # Config class
│
├── setup.py                  # Package setup script
├── README.md                 # Package documentation (this file)
├── requirements.txt          # Dependencies
```

## Contributing

Contributions are welcome! Here’s how you can help:

1. **Fork the repository.**
2. **Create a feature branch:** `git checkout -b my-new-feature`.
3. **Commit your changes:** `git commit -am 'Add some feature'`.
4. **Push to the branch:** `git push origin my-new-feature`.
5. **Submit a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.