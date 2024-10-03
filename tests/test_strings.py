# tests/test_strings.py
import unittest
from pandis import PandisClient
from pandis.exceptions import KeyNotFoundError, InvalidOperationError

class TestStringCommands(unittest.TestCase):
    def setUp(self):
        self.client = PandisClient()

    def test_set_and_get(self):
        self.client.set('name', 'Alice')
        self.assertEqual(self.client.get('name'), 'Alice')

    def test_get_nonexistent_key(self):
        with self.assertRaises(KeyNotFoundError):
            self.client.get('unknown')

    def test_set_overwrite(self):
        self.client.set('key1', 'value1')
        self.client.set('key1', 'value2')
        self.assertEqual(self.client.get('key1'), 'value2')

    def test_set_invalid_type(self):
        self.client.lpush('list1', 'item1')
        with self.assertRaises(InvalidOperationError):
            self.client.set('list1', 'value1')

if __name__ == '__main__':
    unittest.main()
