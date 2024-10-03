# pandis/data_structures/base.py
from ..exceptions import KeyNotFoundError, InvalidOperationError

class BaseCommands:
    def _find_key(self, key, expected_type=None):
        """
        Helper method to find a key in the store.
        """
        key_row = self.store[self.store['key'] == key]
        if key_row.empty:
            raise KeyNotFoundError(f"Key '{key}' not found.")
        if expected_type and key_row.iloc[0]['type'] != expected_type:
            raise InvalidOperationError(f"Key '{key}' is not of type '{expected_type}'.")
        return key_row.iloc[0]

    def _set_key(self, key, data_type, value):
        """
        Helper method to set a key in the store.
        """
        value_id = self._generate_value_id()
        self._set_value(value_id, value)
        new_row = {'key': key, 'type': data_type, 'value_id': value_id}
        self.store = self.store._append(new_row, ignore_index=True)

    def _update_value(self, key_row, value):
        """
        Helper method to update the value associated with a key.
        """
        value_id = key_row['value_id']
        self._set_value(value_id, value)
