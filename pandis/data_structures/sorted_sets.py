# pandis/data_structures/sorted_sets.py
import pandas as pd
from .base import BaseCommands
from ..exceptions import KeyNotFoundError, InvalidOperationError

class SortedSetCommands(BaseCommands):
    def zadd(self, key, mapping):
        """
        Add one or more members to a sorted set, or update its score if it already exists.
        """
        with self.lock:
            try:
                key_row = self._find_key(key, expected_type='sorted_set')
                zset_value = self._get_value(key_row['value_id'])
            except KeyNotFoundError:
                # Create new sorted set
                zset_value = pd.DataFrame(columns=['member', 'score'])
                self._set_key(key, 'sorted_set', zset_value)
                key_row = self._find_key(key)
            # Add or update members
            for member, score in mapping.items():
                mask = zset_value['member'] == member
                if zset_value[mask].empty:
                    # Add new member
                    new_entry = pd.DataFrame({'member': [member], 'score': [score]})
                    zset_value = pd.concat([zset_value, new_entry], ignore_index=True)
                else:
                    # Update existing member
                    zset_value.loc[mask, 'score'] = score
            self._update_value(key_row, zset_value)

    def zrange(self, key, start, end, withscores=False):
        """
        Return a range of members in a sorted set, by index.
        """
        with self.lock:
            key_row = self._find_key(key, expected_type='sorted_set')
            zset_value = self._get_value(key_row['value_id'])
            zset_value = zset_value.sort_values(by='score').reset_index(drop=True)
            total = len(zset_value)
            # Adjust negative indices
            start = start + total if start < 0 else start
            end = end + total if end < 0 else end
            # Ensure indices are within bounds
            start = max(start, 0)
            end = min(end, total - 1)
            result_df = zset_value.iloc[start:end+1]
            if withscores:
                return list(zip(result_df['member'], result_df['score']))
            else:
                return result_df['member'].tolist()
