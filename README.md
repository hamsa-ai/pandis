# Pandis

Pandis is a Python package that emulates Redis functionalities using pandas as the underlying data store.

## Features

- **Strings**: Simple key-value pairs.
- **Hashes**: Key-value pairs where the value is a hash (dictionary-like).
- **Lists**: Ordered collections.
- **Sets**: Unordered collections of unique elements.
- **Sorted Sets**: Sets ordered by a score.

## Installation

```bash
pip install pandis
```

## Usage
```python
from pandis import PandisClient

client = PandisClient()

# Strings
client.set('key1', 'value1')
print(client.get('key1'))  # Output: value1

# Hashes
client.hset('hash1', 'field1', 'value1')
print(client.hget('hash1', 'field1'))  # Output: value1

# Lists
client.lpush('list1', 'a', 'b', 'c')
print(client.lpop('list1'))  # Output: c

# Sets
client.sadd('set1', 'a', 'b', 'c')
print(client.smembers('set1'))  # Output: ['a', 'b', 'c']

# Sorted Sets
client.zadd('zset1', {'a': 3, 'b': 1, 'c': 2})
print(client.zrange('zset1', 0, -1))  # Output: ['b', 'c', 'a']
```

## Testing
```bash
python -m unittest discover tests
```