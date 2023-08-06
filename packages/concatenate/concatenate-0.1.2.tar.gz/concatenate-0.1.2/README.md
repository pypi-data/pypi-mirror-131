# concatenate
Concatenate two objects of the same type

## Installation
```sh
pip install concatenate
```

## Usage
```python
>>> from concatenate import concatenate
>>>
>>> # int
>>> assert concatenate(123, 456) == 123456
>>> assert concatenate(0xdead, 0xbeef, base=16) == 0xdeadbeef
>>> assert concatenate(0b1010, 0b1100, base=2) == 0b10101100
>>> assert concatenate(0o137, 0o246, base=8) == 0o137246
>>>
>>> # str
>>> assert concatenate('foo', 'bar') == 'foobar'
>>>
>>> # dict
>>> assert concatenate({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
>>>
>>> # list
>>> assert concatenate([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
>>>
>>> # tuple
>>> assert concatenate((1, 2, 3), (4, 5, 6)) == (1, 2, 3, 4, 5, 6)
>>>
>>> # set
>>> assert concatenate({1, 2, 3}, {3, 4, 5}) == {1, 2, 3, 4, 5}
```