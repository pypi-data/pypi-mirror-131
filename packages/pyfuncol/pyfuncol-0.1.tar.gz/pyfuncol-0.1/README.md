# pyfuncol

![CI](https://github.com/Gondolav/pyfuncol/actions/workflows/python-app.yml/badge.svg)
[![GitHub license](https://img.shields.io/github/license/Gondolav/pyfuncol)](https://github.com/Gondolav/pyfuncol/blob/main/LICENSE)

A Python functional collections library. It extends collections built-in types through [Forbidden Fruit](https://github.com/clarete/forbiddenfruit) with useful methods to write functional Python code.

## Installation

`pip install pyfuncol`

## Usage

To use the methods, you just need to import pyfuncol. Some examples:

```python
import pyfuncol

[1, 2, 3, 4].map(lambda x: x * 2).filter(lambda x: x > 4)
# [6, 8]

["abc", "def", "e"].group_by(lambda s: len(s))
# {3: ["abc", "def"], 1: ["e"]}

{"a": 1, "b": 2, "c": 3}.flat_map(lambda kv: {kv[0]: kv[1] ** 2})
# {"a": 1, "b": 4, "c": 9}
```

### API

For lists: `map`, `filter`, `flat_map`, `flatten`, `contains`, `distinct`, `foreach`, `group_by`, `is_empty`, `size`, `find`, `index_of`.

For dictionaries: `map`, `filter`, `flat_map`, `contains`, `foreach`, `is_empty`, `size`, `to_list`.

## Compatibility

Since it depends on [Forbidden Fruit](https://github.com/clarete/forbiddenfruit), it only works on CPython.

## License

pyfuncol is licensed under the [MIT license](LICENSE).
