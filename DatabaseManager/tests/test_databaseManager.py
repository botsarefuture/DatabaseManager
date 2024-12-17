
import unittest
from DatabaseManager.databaseManager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """
    Test cases for the DatabaseManager class.
    """

    def setUp(self):
        """
        Set up the test case environment.
        """
        self.database_manager = DatabaseManager.get_instance()

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
        db = self.database_manager.get_db()
        self.assertIsNotNone(db)

    def test_list_collections(self):
        """
        Test listing collections in the default database.
        """
        collections = self.database_manager.list_collections()
        self.assertIsInstance(collections, list)

    def test_get_collection(self):
        """
        Test retrieving a specific collection.
        """
        collection = self.database_manager.get_collection('test_collection')
        self.assertIsNotNone(collection)

    def tearDown(self):
        """
        Clean up after tests.
        """
        self.database_manager.close_connection()

if __name__ == '__main__':
    unittest.main()