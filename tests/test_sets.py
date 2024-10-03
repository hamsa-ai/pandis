# tests/test_sets.py
import unittest
from pandis import PandisClient
from pandis.exceptions import KeyNotFoundError, InvalidOperationError

class TestSetCommands(unittest.TestCase):
    def setUp(self):
        self.client = PandisClient()

    def test_sadd_and_smembers(self):
        self.client.sadd('fruits', 'apple', 'banana', 'cherry')
        self.assertEqual(set(self.client.smembers('fruits')), {'apple', 'banana', 'cherry'})

    def test_srem(self):
        self.client.sadd('fruits', 'apple', 'banana', 'cherry')
        self.client.srem('fruits', 'banana')
        self.assertEqual(set(self.client.smembers('fruits')), {'apple', 'cherry'})

    def test_set_operations_on_non_set(self):
        self.client.set('key1', 'value1')
        with self.assertRaises(InvalidOperationError):
            self.client.sadd('key1', 'value2')

if __name__ == '__main__':
    unittest.main()
