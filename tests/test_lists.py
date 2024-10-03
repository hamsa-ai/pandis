# tests/test_lists.py
import unittest
from pandis import PandisClient
from pandis.exceptions import KeyNotFoundError, InvalidOperationError

class TestListCommands(unittest.TestCase):
    def setUp(self):
        self.client = PandisClient()

    def test_lpush_and_lpop(self):
        self.client.lpush('numbers', 1, 2, 3)
        self.assertEqual(self.client.lpop('numbers'), 3)
        self.assertEqual(self.client.lpop('numbers'), 2)
        self.assertEqual(self.client.lpop('numbers'), 1)
        self.assertIsNone(self.client.lpop('numbers'))

    def test_rpush_and_rpop(self):
        self.client.rpush('letters', 'a', 'b', 'c')
        self.assertEqual(self.client.rpop('letters'), 'c')
        self.assertEqual(self.client.rpop('letters'), 'b')
        self.assertEqual(self.client.rpop('letters'), 'a')
        self.assertIsNone(self.client.rpop('letters'))

    def test_lrange(self):
        self.client.rpush('items', 'item1', 'item2', 'item3', 'item4')
        self.assertEqual(self.client.lrange('items', 1, 2), ['item2', 'item3'])

    def test_list_operations_on_non_list(self):
        self.client.set('key1', 'value1')
        with self.assertRaises(InvalidOperationError):
            self.client.lpush('key1', 'value2')

if __name__ == '__main__':
    unittest.main()
