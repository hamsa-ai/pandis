# pandis/client.py
try:
    import cudf.pandas
    cudf.pandas.install()
    GPU_ENABLED = True    
except ImportError:
    GPU_ENABLED = False

import threading
import pandas as pd
from .data_structures.strings import StringCommands
from .data_structures.hashes import HashCommands
from .data_structures.lists import ListCommands
from .data_structures.sets import SetCommands
from .data_structures.sorted_sets import SortedSetCommands
from .exceptions import KeyNotFoundError, InvalidOperationError

class PandisClient(
    StringCommands,
    HashCommands,
    ListCommands,
    SetCommands,
    SortedSetCommands
):
    """
    PandisClient provides an interface similar to Redis, backed by pandas data structures.
    """
    def __init__(self):
        # Main store DataFrame with columns: 'key', 'type', 'value_id'
        self.store = pd.DataFrame(columns=['key', 'type', 'value_id'])
        # Separate dictionary to hold actual data values
        self.data = {}
        self.lock = threading.Lock()
        # Unique identifier counter for values
        self._id_counter = 0

    def _generate_value_id(self):
        self._id_counter += 1
        return self._id_counter

    def _get_value(self, value_id):
        return self.data.get(value_id)

    def _set_value(self, value_id, value):
        self.data[value_id] = value

    def _delete_value(self, value_id):
        del self.data[value_id]