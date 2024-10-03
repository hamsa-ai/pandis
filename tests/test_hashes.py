# tests/test_hashes.py
import unittest
from pandis import PandisClient
from pandis.exceptions import KeyNotFoundError, InvalidOperationError

class TestHashCommands(unittest.TestCase):
    def setUp(self):
        self.client = PandisClient()

    def test_hset_and_hget(self):
        self.client.hset('user:1', 'name', 'Bob')
        self.client.hset('user:1', 'age', '30')
        self.assertEqual(self.client.hget('user:1', 'name'), 'Bob')
        self.assertEqual(self.client.hget('user:1', 'age'), '30')

    def test_hget_nonexistent_field(self):
        self.client.hset('user:2', 'name', 'Charlie')
        with self.assertRaises(KeyNotFoundError):
            self.client.hget('user:2', 'email')

    def test_hset_on_non_hash(self):
        self.client.set('key1', 'value1')
        with self.assertRaises(InvalidOperationError):
            self.client.hset('key1', 'field', 'value')

if __name__ == '__main__':
    unittest.main()
