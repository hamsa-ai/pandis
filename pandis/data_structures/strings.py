# pandis/data_structures/strings.py
import pandas as pd
from .base import BaseCommands
from ..exceptions import KeyNotFoundError, InvalidOperationError

class StringCommands(BaseCommands):
    def set(self, key, value):
        """
        Set the string value of a key.
        """
        with self.lock:
            # Check if key exists
            try:
                key_row = self._find_key(key)
                if key_row['type'] != 'string':
                    raise InvalidOperationError(f"Key '{key}' is not a string.")
                self._update_value(key_row, value)
            except KeyNotFoundError:
                # Create new key
                self._set_key(key, 'string', value)

    def get(self, key):
        """
        Get the value of a key.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='string')
            value_id = key_row['value_id']
            return self._get_value(value_id)
