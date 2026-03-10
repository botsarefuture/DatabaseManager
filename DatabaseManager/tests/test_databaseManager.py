import unittest
from unittest import mock

from DatabaseManager.databaseManager import DatabaseManager


class DummyConfig:
    MONGO_URI = "mongodb://example:27017"
    MONGO_DBNAME = "dummydb"


class TestDatabaseManager(unittest.TestCase):
    """
    Test cases for the DatabaseManager class.
    """

    def setUp(self):
        """
        Set up the test case environment.
        """
        DatabaseManager._instance = None
        self.database_manager = None

    def _mock_client(self):
        client = mock.MagicMock()
        client.admin.command.return_value = {"ok": 1}
        db = mock.MagicMock()
        client.__getitem__.return_value = db
        db.list_collection_names.return_value = ["test_collection"]
        db.__getitem__.return_value = mock.MagicMock()
        return client, db

    def test_instantiation_does_not_load_config_or_connect(self):
        """
        Instantiation should not load config or open a MongoDB connection.
        """
        with mock.patch.object(DatabaseManager, "_load_config", side_effect=RuntimeError("should not load")), \
                mock.patch("DatabaseManager.databaseManager.MongoClient") as mock_client:
            self.database_manager = DatabaseManager.get_instance()
            self.assertIsNotNone(self.database_manager)
            mock_client.assert_not_called()

    def test_singleton_instance(self):
        """
        Test that DatabaseManager returns the same instance.
        """
        instance1 = DatabaseManager.get_instance()
        instance2 = DatabaseManager.get_instance()
        self.assertIs(instance1, instance2)

    def test_get_db(self):
        """
        Test retrieving a database instance.
        """
        with mock.patch.object(DatabaseManager, "_load_config", return_value=DummyConfig()) as load_config, \
                mock.patch("DatabaseManager.databaseManager.MongoClient") as mock_client:
            client, db = self._mock_client()
            mock_client.return_value = client
            self.database_manager = DatabaseManager.get_instance()
            result = self.database_manager.get_db()
            self.assertIs(result, db)
            load_config.assert_called_once()

    def test_list_collections(self):
        """
        Test listing collections in the default database.
        """
        with mock.patch.object(DatabaseManager, "_load_config", return_value=DummyConfig()), \
                mock.patch("DatabaseManager.databaseManager.MongoClient") as mock_client:
            client, _db = self._mock_client()
            mock_client.return_value = client
            self.database_manager = DatabaseManager.get_instance()
            collections = self.database_manager.list_collections()
            self.assertEqual(collections, ["test_collection"])

    def test_get_collection(self):
        """
        Test retrieving a specific collection.
        """
        with mock.patch.object(DatabaseManager, "_load_config", return_value=DummyConfig()), \
                mock.patch("DatabaseManager.databaseManager.MongoClient") as mock_client:
            client, db = self._mock_client()
            mock_client.return_value = client
            self.database_manager = DatabaseManager.get_instance()
            collection = self.database_manager.get_collection("test_collection")
            self.assertIsNotNone(collection)
            db.__getitem__.assert_called_with("test_collection")

    def tearDown(self):
        """
        Clean up after tests.
        """
        if self.database_manager is not None:
            self.database_manager.close_connection()

if __name__ == '__main__':
    unittest.main()
