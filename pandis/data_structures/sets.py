# pandis/data_structures/sets.py
import pandas as pd
from .base import BaseCommands
from ..exceptions import KeyNotFoundError, InvalidOperationError

class SetCommands(BaseCommands):
    def sadd(self, key, *members):
        """
        Add one or more members to a set.
        """
        with self.lock:
            members = set(members)
            try:
                key_row = self._find_key(key, expected_type='set')
                set_value = self._get_value(key_row['value_id'])
            except KeyNotFoundError:
                # Create new set
                set_value = set()
                self._set_key(key, 'set', set_value)
                key_row = self._find_key(key)
            # Add members
            set_value.update(members)
            self._update_value(key_row, set_value)

    def smembers(self, key):
        """
        Get all the members in a set.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='set')
            set_value = self._get_value(key_row['value_id'])
            return list(set_value)

    def srem(self, key, *members):
        """
        Remove one or more members from a set.
        """
        with self.lock:
            members = set(members)
            key_row = self._find_key(key, expected_type='set')
            set_value = self._get_value(key_row['value_id'])
            set_value.difference_update(members)
            self._update_value(key_row, set_value)
