# DatabaseManager

A simple Python package for managing MongoDB connections using `pymongo`. This package provides a convenient interface for initializing and accessing MongoDB databases with minimal setup.

## Features

- **Easy to use:** Simplifies MongoDB connection initialization.
- **Configurable:** Uses a config file for MongoDB URI and database name.
- **Error handling:** Catches and raises errors if the connection fails or is misconfigured.

## Requirements

- Python 3.7+
- `pymongo`

## Installation

1. **Clone the Repository**

   First, clone the repository (or download it):

   ```bash
   git clone https://github.com/botsarefuture/DatabaseManager.git
   cd DatabaseManager
   ```

2. **Install the Package**

   Install the package and its dependencies using `pip`:

   ```bash
   pip install .
   ```

3. **Install from PyPI (Optional)**

   If the package is uploaded to PyPI, you can install it directly:

   ```bash
   pip install DatabaseManager
   ```

## Usage

### Setup Configuration

Before using the package, you need to set up your configuration for MongoDB. The configuration should be managed via a `config.py` file that contains your `MONGO_URI` and `MONGO_DBNAME`.

Example `config.py`:

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'your_database_name'
```

### Basic Example

```python
from DatabaseManager import DatabaseManager

# Initialize the Database Manager
db_manager = DatabaseManager()

# Get the MongoDB database instance
db = db_manager.get_db()

# Now you can use the `db` object to interact with your MongoDB collections
collection = db['your_collection_name']
document = collection.find_one({"key": "value"})
print(document)
```

### Error Handling

If the database connection fails or is not configured correctly, the package will raise an appropriate error.

```python
try:
    db_manager = DatabaseManager()
    db = db_manager.get_db()
except RuntimeError as e:
    print(f"Error: {e}")
```

## Directory Structure

The package is structured as follows:

```
DatabaseManager/
│
├── DatabaseManager/
│   ├── __init__.py           # Package initialization
│   ├── databaseManager.py    # The DatabaseManager class
│
├── setup.py                  # Package setup script
├── README.md                 # Package documentation (this file)
├── requirements.txt          # Dependencies
```

## Configuration Details

### `Config` Class

The `Config` class is used to store the MongoDB connection details.

Example:

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'my_database'
```

This `Config` class should either be located in your project or passed into the `DatabaseManager` to load your MongoDB settings. The `DatabaseManager` expects these two attributes:

- `MONGO_URI`: MongoDB connection string.
- `MONGO_DBNAME`: Name of the database you want to connect to.

### Environment Variables (Optional)

Instead of hardcoding your configuration, you can also use environment variables to keep sensitive data secure. Update your `config.py` to read from environment variables:

```python
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'your_database_name')
```

Set environment variables:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DBNAME="my_database"
```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This version omits unit tests and focuses on the core functionality and setup of the package.