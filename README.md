# 3db - three DB

[![Build Status](https://travis-ci.org/EvgenyAK/3db.svg?branch=master)](https://travis-ci.org/EvgenyAK/3db.svg?branch=master)

ThreeDB is a lightweight database optimized for data storage used testing.  [DDT](https://en.wikipedia.org/wiki/Data-driven_testing).

## Usage

```
TestData/
    10001_A/
        data_1.txt
        etalon_1.txt
    10002_B/
        data_1.txt
        etalon_1.txt
    10003_A_B/
        data_A_1.txt
        etalon_A_1.txt
        data_B_1.txt
        data_B_1.txt
```

```python
import threedb 


db = threedb.connect("TestData/")
items = db.search()
print(items)

>>> {'ref': './10001_A', 'etalon_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b38>, 'tags': [], 'data_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b70>, 'index': '10001_A'}
>>> {'ref': './10002_A_B', 'etalon_1_txt': <threedb.storage.DataItem object at 0x7f7de4563ba8>, 'tags': [], 'data_1_txt': <threedb.storage.DataItem object at 0x7f7de4563be0>, 'index': '10002_A_B'}
>>> {'ref': './10002_B', 'etalon_1_txt': <threedb.storage.DataItem object at 0x7f7de4563c50>, 'tags': [], 'data_1_txt': <threedb.storage.DataItem object at 0x7f7de4563c88>, 'index': '10002_B'}

items = db.search(*("10001_A",))
print(items)

>>> {'ref': './10001_A', 'etalon_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b38>, 'tags': [], 'data_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b70>, 'index': '10001_A'}

first = item[0]["etalon_1_txt"]
print(first.text)

>>> {"name": "Neo"}

print(first.json())

>> {
    "name": "Neo"
}
```


## Database schema

Used to describe the schema of a database.

```json
'schema': {
    'input_data': {
        'match': ['data.*']
    },
    'gold_etalon': {
        'match': ['etalon.*'],
    }
}
```

```python

db = threedb.connect("TestData/")
items = db.search(*("10001_A",))
print(items)

{'tags': [], 'index': '10001_A', 'ref': './10001_A', 'gold_etalon': <threedb.storage.DataItem object at 0x7fbfaff4bc88>, 'input_data': <threedb.storage.DataItem object at 0x7fbfaff4bf28>}


```
## Meta-data file

```
TestData/
    10001_A/
        metadata.yaml # tags: - serviceA

        data_1.txt
        etalon_1.txt
    10002_B/
        data_1.txt
        etalon_1.txt
    10003_A_B/
        data_A_1.txt
        etalon_A_1.txt
        data_B_1.txt
        data_B_1.txt
```

```python
db = threedb.connect("TestData/")
items = db.search(*("serviceA",))
print(items)

>>> {'ref': './10001_A', 'etalon_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b38>, 'tags': ['serviceA'], 'data_1_txt': <threedb.storage.DataItem object at 0x7f7de4563b70>, 'index': '10001_A'}
```
