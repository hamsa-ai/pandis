# pandis/data_structures/lists.py
import pandas as pd
from .base import BaseCommands
from ..exceptions import KeyNotFoundError, InvalidOperationError

class ListCommands(BaseCommands):
    def lpush(self, key, *values):
        """
        Prepend one or multiple values to a list.
        """
        with self.lock:
            values = list(values)
            try:
                key_row = self._find_key(key, expected_type='list')
                list_value = self._get_value(key_row['value_id'])
            except KeyNotFoundError:
                # Create new list
                list_value = pd.Series(dtype=object)
                self._set_key(key, 'list', list_value)
                key_row = self._find_key(key)
            # Prepend values
            list_value = pd.concat([pd.Series(values[::-1]), list_value], ignore_index=True)
            self._update_value(key_row, list_value)

    def rpush(self, key, *values):
        """
        Append one or multiple values to a list.
        """
        with self.lock:
            values = list(values)
            try:
                key_row = self._find_key(key, expected_type='list')
                list_value = self._get_value(key_row['value_id'])
            except KeyNotFoundError:
                # Create new list
                list_value = pd.Series(dtype=object)
                self._set_key(key, 'list', list_value)
                key_row = self._find_key(key)
            # Append values
            list_value = pd.concat([list_value, pd.Series(values)], ignore_index=True)
            self._update_value(key_row, list_value)

    def lpop(self, key):
        """
        Remove and get the first element in a list.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='list')
            list_value = self._get_value(key_row['value_id'])
            if not list_value.empty:
                value = list_value.iloc[0]
                list_value = list_value.iloc[1:].reset_index(drop=True)
                self._update_value(key_row, list_value)
                return value
            else:
                return None

    def rpop(self, key):
        """
        Remove and get the last element in a list.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='list')
            list_value = self._get_value(key_row['value_id'])
            if not list_value.empty:
                value = list_value.iloc[-1]
                list_value = list_value.iloc[:-1].reset_index(drop=True)
                self._update_value(key_row, list_value)
                return value
            else:
                return None

    def lrange(self, key, start, end):
        """
        Get a range of elements from a list.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='list')
            list_value = self._get_value(key_row['value_id'])
            list_size = len(list_value)
            # Adjust negative indices
            start = start + list_size if start < 0 else start
            end = end + list_size if end < 0 else end
            # Ensure indices are within bounds
            start = max(start, 0)
            end = min(end, list_size - 1)
            return list_value.iloc[start:end+1].tolist()
