# tests/test_sorted_sets.py
import unittest
from pandis import PandisClient
from pandis.exceptions import KeyNotFoundError, InvalidOperationError

class TestSortedSetCommands(unittest.TestCase):
    def setUp(self):
        self.client = PandisClient()

    def test_zadd_and_zrange(self):
        self.client.zadd('scores', {'Alice': 50, 'Bob': 75, 'Charlie': 60})
        self.assertEqual(self.client.zrange('scores', 0, -1), ['Alice', 'Charlie', 'Bob'])
        self.assertEqual(
            self.client.zrange('scores', 0, -1, withscores=True),
            [('Alice', 50), ('Charlie', 60), ('Bob', 75)]
        )

    def test_sorted_set_operations_on_non_sorted_set(self):
        self.client.set('key1', 'value1')
        with self.assertRaises(InvalidOperationError):
            self.client.zadd('key1', {'Member1': 100})

if __name__ == '__main__':
    unittest.main()
