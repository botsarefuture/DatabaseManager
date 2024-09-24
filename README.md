# DatabaseManager

**DatabaseManager** is a simple and efficient Python package for managing MongoDB connections using `pymongo`. It offers a user-friendly interface to initialize and access MongoDB databases with minimal setup, making it ideal for developers looking to streamline their database interactions.

## Features

- **User-Friendly:** Simplifies MongoDB connection initialization with a clear interface.
- **Configurable:** Supports configuration via a dedicated file for MongoDB URI and database name.
- **Robust Error Handling:** Automatically catches and raises errors for failed or misconfigured connections.
- **Environment Variable Support:** Easily integrate sensitive data management by using environment variables.

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

   Use `pip` to install the package along with its dependencies:

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

Before using the package, you need to configure your MongoDB settings. Create a `config.py` file that includes your `MONGO_URI` and `MONGO_DBNAME`.

**Example `config.py`:**

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'your_database_name'
```

### Basic Example

Here’s how to get started with the DatabaseManager:

```python
from DatabaseManager import DatabaseManager

# Initialize the Database Manager
db_manager = DatabaseManager()

# Retrieve the MongoDB database instance
db = db_manager.get_db()

# Use the `db` object to interact with your MongoDB collections
collection = db['your_collection_name']
document = collection.find_one({"key": "value"})
print(document)
```

### Error Handling

The package includes error handling for connection issues. If the database connection fails or is misconfigured, an appropriate error will be raised:

```python
try:
    db_manager = DatabaseManager()
    db = db_manager.get_db()
except RuntimeError as e:
    print(f"Error: {e}")
```

## Directory Structure

The package is organized as follows:

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

The `Config` class holds the MongoDB connection parameters. Here’s a simple example:

```python
class Config:
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DBNAME = 'my_database'
```

You can either include this class in your project or pass it to the `DatabaseManager` to load your MongoDB settings. The `DatabaseManager` expects two attributes:

- **`MONGO_URI`:** The MongoDB connection string.
- **`MONGO_DBNAME`:** The name of the database you wish to connect to.

### Environment Variables (Optional)

For enhanced security, you can utilize environment variables to manage sensitive data. Modify your `config.py` to read from environment variables like this:

```python
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'your_database_name')
```

Set your environment variables using:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DBNAME="my_database"
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