# pandis/data_structures/hashes.py
import pandas as pd
from .base import BaseCommands
from ..exceptions import KeyNotFoundError, InvalidOperationError

class HashCommands(BaseCommands):
    def hset(self, key, field, value):
        """
        Set the value of a hash field.
        """
        with self.lock:
            try:
                key_row = self._find_key(key, expected_type='hash')
                hash_value = self._get_value(key_row['value_id'])
            except KeyNotFoundError:
                # Create new hash
                hash_value = pd.DataFrame(columns=['field', 'value'])
                self._set_key(key, 'hash', hash_value)
                key_row = self._find_key(key)
            # Update field
            mask = hash_value['field'] == field
            if hash_value[mask].empty:
                # Add new field
                new_entry = pd.DataFrame({'field': [field], 'value': [value]})
                hash_value = pd.concat([hash_value, new_entry], ignore_index=True)
            else:
                # Update existing field
                hash_value.loc[mask, 'value'] = value
            self._update_value(key_row, hash_value)

    def hget(self, key, field):
        """
        Get the value of a hash field.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='hash')
            hash_value = self._get_value(key_row['value_id'])
            mask = hash_value['field'] == field
            if hash_value[mask].empty:
                raise KeyNotFoundError(f"Field '{field}' not found in hash '{key}'.")
            return hash_value[mask]['value'].iloc[0]
