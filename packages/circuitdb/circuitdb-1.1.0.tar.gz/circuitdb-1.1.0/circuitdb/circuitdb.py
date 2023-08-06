"""
Data set of optimal circuits for Boolean functions that have
specific low arities.
"""
import doctest
import os
import math
import logical

# The private dictionary that represents the data set.
class _db(dict):
    """
    Wrapper class for a circuit data set instance.
    """
    _data = {}

class _om(dict):
    """
    Wrapper class for a base-level operation-to-circuit map.
    """
    def __getitem__(self, truthtable):
        """
        Data retrieval wrapper with normalization. For validation of
        truth table representation, use the `circuitdb` wrapper.
        """
        # Normalize the truth table representation (no validation).
        if all(isinstance(e, tuple) for e in truthtable):
            truthtable = tuple(tuple(map(int, e)) for e in truthtable)
            ls = set(len(e) for e in truthtable)
            if len(ls) == 1 and list(ls)[0] == 1:
                truthtable = tuple(e[0] for e in truthtable)
        else:
            truthtable = tuple(map(int, truthtable))

        # Retrieve the circuit data.
        return super().__getitem__(truthtable)

# Set up containers for each (arity, coarity, operator set) combination
# for which data is included.
for i in range(1, 4):
    _db._data[i] = {}

    if i in range(1, 4):
        _db._data[i][1] = {
            frozenset([logical.id_, logical.not_, logical.and_, logical.or_]): {},
            frozenset([logical.id_, logical.not_, logical.and_, logical.xor_]): {},
            frozenset(logical.every): {}
        }

    if i == 2:
        _db._data[i][2] = {
            frozenset([logical.id_, logical.not_, logical.and_, logical.or_]): {},
            frozenset([logical.id_, logical.not_, logical.and_, logical.xor_]): {},
            frozenset(logical.every): {}
        }

_db._data\
    [1][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = _om({
        (1, 0): [(logical.id_,), (logical.not_, 0), (logical.id_, 1)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (0, 0): [(logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.id_, 2)],
        (1, 1): [(logical.id_,), (logical.not_, 0), (logical.or_, 0, 1), (logical.id_, 2)],
    })

_db._data\
    [2][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = _om({
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.id_, 2)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.id_, 2)],
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 2)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.id_, 2)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5)],
    })

_db._data\
    [2][2]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = _om({
        ((0, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 1)),
        ((0, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.id_, 1), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.id_, 1), (logical.id_, 1)),
        ((0, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 1), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 1), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 1, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 1, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 5)),
        ((0, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.and_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 1, 2), (logical.or_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 1, 2), (logical.or_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 0), (logical.id_, 5)),
        ((0, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 1), (logical.id_, 5)),
        ((0, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 2), (logical.id_, 5)),
        ((1, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 3), (logical.id_, 5)),
        ((0, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 4), (logical.id_, 5)),
        ((0, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 1)),
        ((0, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 3)),
        ((0, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 4)),
        ((0, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 5)),
        ((0, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 0), (logical.id_, 5)),
        ((0, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 1), (logical.id_, 5)),
        ((0, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 2), (logical.id_, 5)),
        ((0, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 3), (logical.id_, 5)),
        ((1, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 1)),
        ((1, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 2)),
        ((1, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 5)),
        ((1, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 2), (logical.id_, 6)),
        ((1, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 3), (logical.id_, 6)),
        ((1, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 2), (logical.id_, 6)),
        ((1, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 3), (logical.id_, 6)),
        ((0, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 4), (logical.id_, 6)),
        ((0, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 5), (logical.id_, 6)),
        ((0, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 2)),
        ((0, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 3)),
        ((0, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 4)),
        ((0, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6), (logical.id_, 5)),
        ((1, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 4), (logical.id_, 6)),
        ((1, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 5), (logical.id_, 6)),
        ((1, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6), (logical.id_, 5)),
        ((0, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 3), (logical.id_, 6)),
        ((1, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 4), (logical.id_, 6)),
        ((0, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6), (logical.id_, 4)),
        ((0, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.id_, 3), (logical.id_, 6)),
        ((1, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6), (logical.id_, 3)),
        ((1, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 4), (logical.id_, 6)),
        ((0, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6), (logical.id_, 4)),
        ((0, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.and_, 3, 5), (logical.id_, 4), (logical.id_, 6)),
        ((0, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.and_, 3, 5), (logical.id_, 6), (logical.id_, 4)),
        ((1, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.and_, 3, 4), (logical.id_, 5), (logical.id_, 6)),
        ((0, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.and_, 3, 4), (logical.id_, 6), (logical.id_, 5)),
        ((1, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 2, 5), (logical.id_, 3), (logical.id_, 6)),
        ((1, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 2, 5), (logical.id_, 6), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 5), (logical.id_, 6)),
        ((1, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6), (logical.id_, 5)),
        ((0, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.or_, 0, 3), (logical.id_, 5), (logical.id_, 6)),
        ((1, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.or_, 0, 3), (logical.id_, 6), (logical.id_, 5)),
        ((0, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.and_, 0, 4), (logical.or_, 2, 4), (logical.id_, 5), (logical.id_, 6)),
        ((1, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.and_, 0, 4), (logical.or_, 2, 4), (logical.id_, 6), (logical.id_, 5)),
        ((1, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.or_, 3, 4), (logical.id_, 5), (logical.id_, 6)),
        ((1, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.or_, 3, 4), (logical.id_, 6), (logical.id_, 5)),
    })

_db._data\
    [3][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.or_])]\
    = _om({
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.id_, 3)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.id_, 3)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.id_, 3)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.id_, 3)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 2, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.or_, 2, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 0, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 0, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.or_, 1, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 1), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 0, 3), (logical.and_, 1, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.or_, 1, 3), (logical.and_, 0, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 1, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 2, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.or_, 1, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.or_, 2, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.or_, 1, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.or_, 1, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 2, 4), (logical.not_, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4), (logical.not_, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 3, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 3, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 3, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 0, 2), (logical.or_, 1, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 1, 2), (logical.or_, 0, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.or_, 0, 1), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.or_, 2, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.or_, 1, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.or_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 2, 3), (logical.or_, 5, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 2, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 3, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 2), (logical.or_, 0, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.and_, 1, 4), (logical.or_, 0, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 4, 5), (logical.or_, 1, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.or_, 0, 2), (logical.or_, 1, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.or_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.and_, 1, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 1, 3), (logical.or_, 5, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 1, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.and_, 0, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 0, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 4, 5), (logical.or_, 0, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.or_, 0, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 1), (logical.or_, 2, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.and_, 0, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 0, 6), (logical.id_, 7)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 0, 2), (logical.and_, 1, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.and_, 3, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.and_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.not_, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.or_, 1, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.and_, 3, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.or_, 0, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.and_, 4, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.and_, 4, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 5, 6), (logical.or_, 3, 7), (logical.id_, 8)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.or_, 1, 2), (logical.or_, 3, 6), (logical.and_, 5, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.or_, 1, 2), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 5), (logical.or_, 4, 6), (logical.and_, 3, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 3, 5), (logical.or_, 4, 6), (logical.not_, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 3), (logical.or_, 1, 5), (logical.not_, 6), (logical.or_, 4, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 3), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.and_, 2, 5), (logical.not_, 6), (logical.or_, 4, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.or_, 1, 3), (logical.or_, 2, 4), (logical.not_, 6), (logical.and_, 5, 7), (logical.id_, 8)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.and_, 1, 4), (logical.or_, 1, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 1, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.or_, 2, 3), (logical.and_, 1, 5), (logical.not_, 6), (logical.or_, 4, 7), (logical.id_, 8)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 1, 3), (logical.or_, 2, 3), (logical.and_, 1, 5), (logical.not_, 6), (logical.and_, 4, 7), (logical.id_, 8)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.or_, 2, 3), (logical.and_, 1, 4), (logical.or_, 1, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 0, 4), (logical.or_, 0, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.id_, 8)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.or_, 2, 3), (logical.and_, 0, 4), (logical.or_, 0, 4), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.or_, 2, 6), (logical.and_, 5, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 5), (logical.not_, 6), (logical.or_, 4, 7), (logical.id_, 8)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 3), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 3), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 3), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.or_, 1, 3), (logical.not_, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.not_, 4), (logical.or_, 1, 2), (logical.and_, 0, 6), (logical.or_, 5, 7), (logical.id_, 8)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.or_, 1, 2), (logical.and_, 0, 5), (logical.not_, 6), (logical.and_, 4, 7), (logical.id_, 8)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.or_, 0, 1), (logical.and_, 2, 6), (logical.or_, 3, 7), (logical.and_, 5, 8), (logical.id_, 9)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.and_, 2, 5), (logical.or_, 3, 6), (logical.not_, 7), (logical.or_, 4, 8), (logical.id_, 9)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.id_, 9)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.id_, 9)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.not_, 6), (logical.or_, 3, 5), (logical.or_, 7, 8), (logical.id_, 9)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.or_, 2, 4), (logical.or_, 3, 5), (logical.not_, 7), (logical.and_, 6, 8), (logical.id_, 9)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.id_, 9)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.id_, 9)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 1, 2), (logical.and_, 6, 7), (logical.or_, 4, 8), (logical.id_, 9)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.id_, 9)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.and_, 1, 3), (logical.or_, 0, 2), (logical.or_, 1, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.not_, 9), (logical.id_, 10)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.and_, 0, 3), (logical.or_, 0, 3), (logical.not_, 5), (logical.or_, 1, 2), (logical.and_, 6, 7), (logical.or_, 4, 8), (logical.not_, 9), (logical.id_, 10)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 0, 2), (logical.and_, 1, 4), (logical.not_, 5), (logical.or_, 1, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9), (logical.id_, 10)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 0, 1), (logical.and_, 2, 4), (logical.not_, 5), (logical.or_, 2, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9), (logical.id_, 10)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.and_, 0, 4), (logical.not_, 5), (logical.or_, 0, 4), (logical.and_, 6, 7), (logical.or_, 3, 8), (logical.not_, 9), (logical.id_, 10)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.or_, 0, 1), (logical.or_, 2, 3), (logical.not_, 6), (logical.and_, 5, 7), (logical.or_, 4, 8), (logical.not_, 9), (logical.id_, 10)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.or_, 0, 1), (logical.and_, 4, 5), (logical.and_, 2, 6), (logical.not_, 7), (logical.or_, 2, 6), (logical.and_, 8, 9), (logical.id_, 10)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 1, 2), (logical.not_, 4), (logical.or_, 3, 5), (logical.and_, 0, 6), (logical.not_, 7), (logical.or_, 0, 6), (logical.and_, 8, 9), (logical.id_, 10)],
    })

_db._data\
    [1][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = _om({
        (1, 0): [(logical.id_,), (logical.not_, 0), (logical.id_, 1)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (0, 0): [(logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3)],
        (1, 1): [(logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.id_, 2)],
    })

_db._data\
    [2][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = _om({
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.id_, 2)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.id_, 2)],
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 2)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.id_, 2)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 3)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
    })

_db._data\
    [2][2]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = _om({
        ((0, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 0), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 0), (logical.id_, 1)),
        ((0, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 1), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 1), (logical.id_, 1)),
        ((0, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 1), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 1)),
        ((0, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 3)),
        ((1, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.xor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.xor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 0), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 1), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 1)),
        ((1, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 0), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 1), (logical.id_, 4)),
        ((1, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 1)),
        ((1, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 4)),
        ((1, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 0), (logical.id_, 4)),
        ((0, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 1), (logical.id_, 4)),
        ((1, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 4)),
        ((0, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 0), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 1), (logical.id_, 4)),
        ((1, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 1)),
        ((1, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 4)),
        ((0, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 0), (logical.id_, 4)),
        ((0, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 1), (logical.id_, 4)),
        ((1, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 1)),
        ((0, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 4)),
        ((0, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 4)),
        ((0, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 1), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 1, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 1, 3), (logical.id_, 4), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((1, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 2), (logical.id_, 4)),
        ((0, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 4)),
        ((0, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 2), (logical.id_, 4)),
        ((1, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4), (logical.id_, 2)),
        ((0, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 4), (logical.id_, 5)),
        ((0, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.id_, 4), (logical.id_, 5)),
        ((0, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 2), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 1, 2), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.not_, 4), (logical.id_, 3), (logical.id_, 5)),
        ((1, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.not_, 4), (logical.id_, 5), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.xor_, 0, 4), (logical.id_, 3), (logical.id_, 5)),
        ((0, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.and_, 0, 2), (logical.and_, 1, 2), (logical.xor_, 0, 4), (logical.id_, 5), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 2), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 5)),
        ((0, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 1, 2), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.xor_, 0, 3), (logical.id_, 4), (logical.id_, 5)),
        ((0, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.xor_, 0, 3), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.xor_, 1, 2), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.xor_, 1, 2), (logical.id_, 5), (logical.id_, 4)),
        ((0, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 0, 2), (logical.xor_, 2, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 1, 3), (logical.id_, 4), (logical.id_, 5)),
        ((0, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 1, 3), (logical.id_, 5), (logical.id_, 4)),
        ((1, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.id_, 3), (logical.id_, 5)),
        ((0, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.id_, 5), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 3), (logical.id_, 5)),
        ((1, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 3), (logical.xor_, 1, 3), (logical.id_, 4), (logical.id_, 5)),
        ((1, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.xor_, 0, 3), (logical.xor_, 1, 3), (logical.id_, 5), (logical.id_, 4)),
    })

_db._data\
    [3][1]\
    [frozenset([logical.id_, logical.not_, logical.and_, logical.xor_])]\
    [frozenset([logical.and_])]\
    = _om({
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.id_, 3)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.id_, 3)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.id_, 3)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.id_, 3)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 0), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.not_, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 4, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.xor_, 2, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.xor_, 1, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 2), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 2, 3), (logical.and_, 1, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 3, 4), (logical.and_, 0, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 0, 3), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.xor_, 2, 3), (logical.and_, 0, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 1), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 2), (logical.and_, 1, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 0, 3), (logical.and_, 1, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 1, 2), (logical.and_, 0, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.xor_, 1, 3), (logical.and_, 0, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 0, 5), (logical.id_, 6)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.xor_, 1, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.xor_, 1, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.xor_, 0, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.xor_, 0, 3), (logical.and_, 4, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 1, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 2, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 3, 4), (logical.not_, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 0, 2), (logical.xor_, 3, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.and_, 3, 5), (logical.xor_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 1, 2), (logical.xor_, 4, 5), (logical.and_, 3, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 4), (logical.xor_, 1, 5), (logical.and_, 3, 6), (logical.id_, 7)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 0, 1), (logical.xor_, 3, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 2), (logical.and_, 3, 5), (logical.xor_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.and_, 4, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 1, 3), (logical.xor_, 5, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 3, 4), (logical.and_, 2, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 3, 4), (logical.and_, 1, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 2), (logical.and_, 3, 4), (logical.xor_, 1, 2), (logical.xor_, 5, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.not_, 4), (logical.xor_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 1, 3), (logical.xor_, 0, 4), (logical.and_, 2, 5), (logical.xor_, 4, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.not_, 4), (logical.xor_, 1, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 2, 3), (logical.xor_, 0, 4), (logical.and_, 1, 5), (logical.xor_, 4, 6), (logical.id_, 7)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 1), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 0, 2), (logical.xor_, 1, 2), (logical.and_, 4, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.xor_, 1, 3), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.not_, 6), (logical.id_, 7)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.and_, 4, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 2), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.not_, 4), (logical.xor_, 2, 3), (logical.and_, 5, 6), (logical.id_, 7)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.and_, 2, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 3), (logical.xor_, 1, 4), (logical.and_, 2, 5), (logical.xor_, 4, 6), (logical.id_, 7)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5), (logical.not_, 6), (logical.id_, 7)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.and_, 0, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 0, 6), (logical.id_, 7)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 3, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 2, 4), (logical.and_, 1, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 2, 4), (logical.and_, 0, 5), (logical.xor_, 3, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.and_, 2, 4), (logical.xor_, 0, 1), (logical.xor_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 2), (logical.and_, 4, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.xor_, 2, 4), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 1, 4), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 3), (logical.and_, 4, 5), (logical.xor_, 1, 6), (logical.id_, 7)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.not_, 3), (logical.xor_, 0, 1), (logical.and_, 4, 5), (logical.xor_, 2, 6), (logical.id_, 7)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.not_, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 0, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 1, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.not_, 2), (logical.and_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 2, 7), (logical.id_, 8)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 1), (logical.and_, 2, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.not_, 2), (logical.and_, 1, 3), (logical.xor_, 0, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.and_, 2, 5), (logical.xor_, 1, 3), (logical.xor_, 6, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.not_, 4), (logical.xor_, 1, 2), (logical.and_, 5, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 2, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.xor_, 3, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.xor_, 1, 5), (logical.xor_, 4, 5), (logical.and_, 6, 7), (logical.id_, 8)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.xor_, 1, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.not_, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.not_, 2), (logical.and_, 0, 3), (logical.xor_, 1, 5), (logical.and_, 4, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.xor_, 2, 4), (logical.and_, 5, 6), (logical.xor_, 3, 7), (logical.id_, 8)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.not_, 3), (logical.xor_, 0, 1), (logical.xor_, 3, 5), (logical.and_, 2, 6), (logical.xor_, 4, 7), (logical.id_, 8)],
    })

_db._data\
    [1][1]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = _om({
        (0, 0): [(logical.id_,), (logical.uf_, 0), (logical.id_, 1)],
        (0, 1): [(logical.id_,), (logical.id_, 0)],
        (1, 0): [(logical.id_,), (logical.not_, 0), (logical.id_, 1)],
        (1, 1): [(logical.id_,), (logical.ut_, 0), (logical.id_, 1)],
    })

_db._data\
    [2][1]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = _om({
        (0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.fst_, 0, 1), (logical.id_, 2)],
        (0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.snd_, 0, 1), (logical.id_, 2)],
        (1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.nfst_, 0, 1), (logical.id_, 2)],
        (1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.nsnd_, 0, 1), (logical.id_, 2)],
        (0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.bf_, 0, 1), (logical.id_, 2)],
        (1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.bt_, 0, 1), (logical.id_, 2)],
        (0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 2)],
        (0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.id_, 2)],
        (1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.id_, 2)],
        (0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.nif_, 0, 1), (logical.id_, 2)],
        (0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.id_, 2)],
        (1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.id_, 2)],
        (0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.id_, 2)],
        (1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.nand_, 0, 1), (logical.id_, 2)],
        (1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.xnor_, 0, 1), (logical.id_, 2)],
        (1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.imp_, 0, 1), (logical.id_, 2)],
    })

_db._data\
    [2][2]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = _om({
        ((0, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.id_, 0), (logical.id_, 1)),
        ((0, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.uf_, 0), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.id_, 1), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.id_, 1), (logical.id_, 1)),
        ((0, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.uf_, 0), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.uf_, 0), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.uf_, 0), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.uf_, 0), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.ut_, 0), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.ut_, 0), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.ut_, 0), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.ut_, 0), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.ut_, 0), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (1, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.nor_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.nor_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.nor_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.nor_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((0, 0), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((0, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.nand_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.nand_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.imp_, 0, 1), (logical.id_, 0), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.imp_, 0, 1), (logical.id_, 1), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 0)),
        ((1, 0), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 1)),
        ((1, 1), (1, 1), (0, 0), (1, 1)):(0, 1, (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.not_, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.xnor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.xnor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nif_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nif_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nif_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.not_, 0), (logical.if_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.if_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.nor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.not_, 0), (logical.nimp_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.not_, 0), (logical.nimp_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.not_, 0), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 0), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.xnor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.xnor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nif_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.not_, 1), (logical.nif_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nif_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nimp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.nimp_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.nimp_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.not_, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.not_, 1), (logical.nand_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.not_, 1), (logical.nand_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.nif_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.nif_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.nif_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.nor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.nor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (1, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.xnor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.xnor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.nif_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.nif_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.or_, 0, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.or_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.or_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 1), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 1), (1, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 1), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.bt_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 1), (0, 1), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 1), (1, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 0), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (0, 1), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 0), (0, 0)):(0, 1, (logical.nif_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (0, 0), (0, 1)):(0, 1, (logical.nif_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 0), (1, 0)):(0, 1, (logical.nif_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.bt_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.bt_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 0), (1, 1), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.if_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (1, 1), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.if_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 0), (1, 0), (1, 0)):(0, 1, (logical.bt_, 0, 1), (logical.nor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 1), (0, 1), (0, 1)):(0, 1, (logical.bt_, 0, 1), (logical.nor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.bt_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.bt_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (1, 1), (1, 0)):(0, 1, (logical.bt_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (1, 1), (0, 1)):(0, 1, (logical.bt_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (1, 0), (1, 0), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 1), (0, 1), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 1), (1, 0)):(0, 1, (logical.bt_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (1, 1), (0, 1)):(0, 1, (logical.bt_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 0), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 1), (1, 1)):(0, 1, (logical.bt_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 0), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.if_, 0, 1), (logical.nif_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.if_, 0, 1), (logical.nif_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 0), (1, 0)):(0, 1, (logical.if_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 1), (0, 1)):(0, 1, (logical.if_, 0, 1), (logical.bf_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.if_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.if_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 1), (1, 0)):(0, 1, (logical.if_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 1), (0, 1)):(0, 1, (logical.if_, 0, 1), (logical.xor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (1, 1), (1, 0)):(0, 1, (logical.if_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 1), (0, 1)):(0, 1, (logical.if_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (1, 0), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 1), (1, 1)):(0, 1, (logical.if_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (0, 0), (0, 0), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nimp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.bf_, 0, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.bf_, 0, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.bf_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.bf_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.bf_, 0, 1), (logical.imp_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 1), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (1, 0), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.xnor_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (0, 0), (0, 1)):(0, 1, (logical.nor_, 0, 1), (logical.or_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (0, 0), (1, 0)):(0, 1, (logical.nor_, 0, 1), (logical.or_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.xor_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 0), (0, 0), (0, 0), (0, 1)):(0, 1, (logical.nor_, 0, 1), (logical.and_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((0, 1), (0, 0), (0, 0), (1, 0)):(0, 1, (logical.nor_, 0, 1), (logical.and_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (0, 1), (0, 1), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 0), (1, 0), (0, 0)):(0, 1, (logical.nor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.nif_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.if_, 1, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.if_, 1, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.xor_, 0, 1), (logical.nimp_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.xor_, 0, 1), (logical.nimp_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 1), (1, 1), (0, 0)):(0, 1, (logical.xor_, 0, 1), (logical.nand_, 0, 1), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 0), (0, 1)):(0, 1, (logical.nimp_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 1), (1, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (1, 1), (0, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 1), (0, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 0), (0, 0), (1, 0), (0, 1)):(0, 1, (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((0, 0), (0, 0), (0, 1), (1, 0)):(0, 1, (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (0, 1), (1, 0)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (1, 0), (0, 1)):(0, 1, (logical.and_, 0, 1), (logical.not_, 2), (logical.id_, 3), (logical.id_, 2)),
        ((0, 1), (0, 1), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 0), (1, 0), (0, 0), (1, 1)):(0, 1, (logical.and_, 0, 1), (logical.xnor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
        ((1, 1), (1, 1), (1, 0), (0, 1)):(0, 1, (logical.nand_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 2), (logical.id_, 3)),
        ((1, 1), (1, 1), (0, 1), (1, 0)):(0, 1, (logical.nand_, 0, 1), (logical.xor_, 0, 2), (logical.id_, 3), (logical.id_, 2)),
    })

_db._data\
    [3][1]\
    [frozenset(logical.every)]\
    [frozenset(logical.every)]\
    = _om({
        (0, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 0)],
        (0, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 1)],
        (0, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.id_, 2)],
        (1, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 0), (logical.id_, 3)],
        (1, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.not_, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.uf_, 0), (logical.id_, 3)],
        (1, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.ut_, 0), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.id_, 3)],
        (0, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.id_, 3)],
        (0, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.id_, 3)],
        (0, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.id_, 3)],
        (1, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.id_, 3)],
        (1, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 0, 1), (logical.id_, 3)],
        (0, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 0, 2), (logical.id_, 3)],
        (0, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nif_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.id_, 3)],
        (0, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.id_, 3)],
        (0, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.id_, 3)],
        (1, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.id_, 3)],
        (1, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.id_, 3)],
        (0, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 1), (logical.id_, 3)],
        (0, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 0, 2), (logical.id_, 3)],
        (0, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.or_, 1, 2), (logical.id_, 3)],
        (1, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 0, 1), (logical.id_, 3)],
        (1, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 0, 2), (logical.id_, 3)],
        (1, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nand_, 1, 2), (logical.id_, 3)],
        (1, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 0, 1), (logical.id_, 3)],
        (1, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 0, 2), (logical.id_, 3)],
        (1, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xnor_, 1, 2), (logical.id_, 3)],
        (1, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 0, 1), (logical.id_, 3)],
        (1, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 0, 2), (logical.id_, 3)],
        (1, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.imp_, 1, 2), (logical.id_, 3)],
        (0, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nif_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nand_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xnor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.imp_, 2, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nif_, 1, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xnor_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.imp_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.if_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nif_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xnor_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.imp_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.if_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nif_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nor_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xnor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.imp_, 2, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nor_, 1, 3), (logical.id_, 4)],
        (0, 0, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xnor_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.imp_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nimp_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.if_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nif_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.nor_, 0, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xnor_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.imp_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.nif_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.nand_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.xnor_, 2, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nif_, 1, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nor_, 1, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.nand_, 1, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.xnor_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.nif_, 0, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.nand_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.xnor_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.and_, 2, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nimp_, 2, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.if_, 2, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nif_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nand_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xnor_, 2, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.imp_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.and_, 1, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nimp_, 1, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.if_, 1, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nif_, 1, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 1, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nand_, 1, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.imp_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.and_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nimp_, 0, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.if_, 0, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nif_, 0, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nand_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.imp_, 0, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nimp_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.if_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nif_, 2, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.xor_, 2, 3), (logical.id_, 4)],
        (0, 0, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.nor_, 2, 3), (logical.id_, 4)],
        (1, 1, 0, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.or_, 2, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.xnor_, 2, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 1), (logical.imp_, 2, 3), (logical.id_, 4)],
        (0, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.nimp_, 1, 3), (logical.id_, 4)],
        (1, 0, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.xor_, 1, 3), (logical.id_, 4)],
        (0, 1, 0, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.nor_, 1, 3), (logical.id_, 4)],
        (1, 0, 1, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.or_, 1, 3), (logical.id_, 4)],
        (0, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.xnor_, 1, 3), (logical.id_, 4)],
        (1, 1, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 0, 2), (logical.imp_, 1, 3), (logical.id_, 4)],
        (0, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.nimp_, 0, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.xor_, 0, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 0, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.nor_, 0, 3), (logical.id_, 4)],
        (1, 0, 0, 0, 1, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.or_, 0, 3), (logical.id_, 4)],
        (0, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.xnor_, 0, 3), (logical.id_, 4)],
        (1, 1, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nor_, 1, 2), (logical.imp_, 0, 3), (logical.id_, 4)],
        (0, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 0, 4), (logical.id_, 5)],
        (1, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 1, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 0, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 0, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 1, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.if_, 1, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 1, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 0, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nor_, 1, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.xnor_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 0, 1), (logical.if_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.if_, 0, 1), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nor_, 1, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 1), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 1), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 2), (logical.xor_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nor_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.nimp_, 2, 3), (logical.xnor_, 0, 4), (logical.id_, 5)],
        (1, 0, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 1, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 1), (logical.xor_, 1, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.nimp_, 1, 3), (logical.xnor_, 0, 4), (logical.id_, 5)],
        (1, 1, 0, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 0, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 1), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 1), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.nimp_, 1, 2), (logical.xor_, 0, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.and_, 2, 3), (logical.xnor_, 1, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3), (logical.xor_, 1, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 1), (logical.if_, 2, 3), (logical.xnor_, 1, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xor_, 0, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xnor_, 0, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 0, 2), (logical.if_, 1, 3), (logical.xnor_, 2, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3), (logical.xor_, 2, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.if_, 1, 2), (logical.if_, 0, 3), (logical.xnor_, 2, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.and_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nimp_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.if_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nif_, 3, 4), (logical.id_, 5)],
        (1, 0, 0, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.nand_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.xor_, 0, 2), (logical.imp_, 3, 4), (logical.id_, 5)],
        (0, 1, 0, 0, 0, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 0, 2), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 0, 1, 1, 1, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 1), (logical.nor_, 0, 2), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 0, 1, 0, 0, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 1, 0, 1, 1, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 0, 2), (logical.nor_, 0, 1), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 0, 0, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 1), (logical.nor_, 3, 4), (logical.id_, 5)],
        (1, 1, 1, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.xor_, 1, 2), (logical.nor_, 0, 1), (logical.or_, 3, 4), (logical.id_, 5)],
        (0, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 1), (logical.xor_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.xor_, 0, 1), (logical.xnor_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 1, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 1, 0, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.nimp_, 2, 3), (logical.nor_, 0, 1), (logical.xnor_, 4, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 1, 1, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.xor_, 3, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 1, 0, 0, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 0, 1), (logical.and_, 2, 4), (logical.nor_, 3, 5), (logical.id_, 6)],
        (0, 0, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.nimp_, 4, 5), (logical.id_, 6)],
        (0, 0, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 1, 0, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.or_, 4, 5), (logical.id_, 6)],
        (1, 1, 1, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 1), (logical.xor_, 2, 3), (logical.nor_, 0, 1), (logical.imp_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 0, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 1, 1, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.nimp_, 1, 3), (logical.nor_, 0, 2), (logical.xnor_, 4, 5), (logical.id_, 6)],
        (0, 1, 0, 0, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.nor_, 0, 2), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 0, 1, 1, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 0, 2), (logical.xor_, 1, 3), (logical.nor_, 0, 2), (logical.or_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 0, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.xor_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 0, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 1, 1, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.nimp_, 0, 3), (logical.nor_, 1, 2), (logical.xnor_, 4, 5), (logical.id_, 6)],
        (0, 1, 1, 0, 0, 0, 0, 1): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.nor_, 1, 2), (logical.nor_, 4, 5), (logical.id_, 6)],
        (1, 0, 0, 1, 1, 1, 1, 0): [(logical.id_,), (logical.id_,), (logical.id_,), (logical.and_, 1, 2), (logical.xor_, 0, 3), (logical.nor_, 1, 2), (logical.or_, 4, 5), (logical.id_, 6)],
    })

class circuitdb(dict):
    """
    Wrapper class for a circuit data set that contains an (arbitrary but fixed)
    example of the smallest possible logical circuit (in terms of the number of
    unary and/or binary gates) for each possible logical function (from a finite
    set of functions). This class supports both a dictionary-like interface
    (inherited from the ``dict`` type) and a function-like interface (via the
    :obj:`__call__` method).

    **Logical Function Representation:** Logical functions are represented using
    tuples, as in the `logical <https://pypi.org/project/logical/>`_ library. For
    example, the logical function *f* (*x*, *y*, *z*) = *x* **and** *y* **and** *z*
    (*i.e.*, three-argument conjunction) is represented using a tuple representation
    of the output column of the truth table for the function (assuming that the
    possible inputs are in ascending dictionary order): ``(0, 0, 0, 0, 0, 0, 0, 1)``.

    >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 1))
    [((0, 1),), ((0, 1),), ((0, 1),), ((0, 0, 0, 1), 0, 1), ((0, 0, 0, 1), 2, 3), ((0, 1), 4)]

    For logical functions having multiple outputs, the entries in the tuple may
    themselves be tuples. For example, *f* (*x*, *y*) = (*y*, *x*) is represented
    using the tuple ``((0, 0), (1, 0), (0, 1), (1, 1))``.

    >>> circuitdb(((0, 0), (1, 0), (0, 1), (1, 1)))
    [0, 1, ((0, 1), 1), ((0, 1), 0)]

    **Circuit Representation:** The representation of a circuit consists of a list
    of unary and binary gates. Each gate is represented as a tuple. The first entry
    in each gate tuple is the logical function corresponding to that gate (represented
    as in the `logical <https://pypi.org/project/logical/>`_ library). The remaining
    entries in the gate tuple are the indices of the input gates to that gate.

    >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 1))
    [((0, 1),), ((0, 1),), ((0, 1),), ((0, 0, 0, 1), 0, 1), ((0, 0, 0, 1), 2, 3), ((0, 1), 4)]

    In the circuit above, the entry ``((0, 0, 0, 1), 2, 3)`` represents a gate that
    is a conjunction (*i.e.*, ``(0, 0, 0, 1)``) of the gates at positions ``2`` and
    ``3`` in the overall list (*i.e.* , ``((0, 1),)`` and ``((0, 0, 0, 1), 0, 1)``).

    **Set of Permitted Gates:** For any given logical function, it is possible to
    construct a corresponding circuit using a variety of gate sets. For each logical
    function, the database contains an example of a smallest circuit for each of a
    small collection of sets of unary and binary gates. The set of gates that can be
    used to construct a circuit can be supplied using the ``operators`` parameter.
    In the remaining examples below, circuits are retrieved for the specific function
    ``(0, 0, 1, 0, 0, 0, 0, 1)``. The unary and binary logical operators represented
    by the gates in the circuit below are drawn from the set of permitted gates
    ``{logical.id_, logical.not_, logical.and_, logical.or_}``.

    >>> from logical import logical
    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1), frozenset([logical.id_, logical.not_, logical.and_, logical.or_]))
    [((0, 1),), ((0, 1),), ((0, 1),), ((0, 0, 0, 1), 0, 2), ((0, 1, 1, 1), 0, 2), ((1, 0), 4), ((0, 1, 1, 1), 3, 5), ((0, 0, 0, 1), 1, 6), ((0, 1), 7)]

    All gates in the circuit below are found in the set
    ``{logical.id_, logical.not_, logical.and_, logical.xor_}``.

    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1), frozenset([logical.id_, logical.not_, logical.and_, logical.xor_]))
    [((0, 1),), ((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 1, 1, 0), 2, 3), ((0, 0, 0, 1), 1, 4), ((0, 1), 5)]

    By default (or if the set of all gates ``logical.every`` is specified), a smallest circuit that can be built using *any* combination of unary or binary gates is returned.

    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1))
    [((0, 1),), ((0, 1),), ((0, 1),), ((0, 1, 1, 0), 0, 2), ((0, 0, 1, 0), 1, 3), ((0, 1), 4)]

    **Set of Gates to Minimize:** Multiple possible circuits that use gates from
    a given gate set can be used to implement a logical function. Some of these
    circuits may have more of one type of gate than other circuits. Thus, there
    is an option to specify which gates "count" towards the size of the circuit
    (with all other gates not counted for the purposes of comparing circuits
    according to their size) using the ``minimize`` parameter.

    >>> circuitdb((0, 0, 1, 0, 0, 0, 0, 1), frozenset([logical.id_, logical.not_, logical.and_, logical.xor_]), {logical.and_})
    [((0, 1),), ((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 1, 1, 0), 2, 3), ((0, 0, 0, 1), 1, 4), ((0, 1), 5)]

    **Supported Combinations:** Each logical function has a number of input values,
    a number of output values, a set of permitted gates/**operators**, and a set of
    gates to **minimize** in quantity. Entries exist in the database for only a finite
    set of logical functions. The table below lists the supported combinations of
    function input count, function output count, and gate set that are found in the
    database. **All** functions for a given combination of inputs and outputs are
    supported (*e.g.*, all ``2**(2**3) = 256`` functions having three inputs and one
    output are supported). Gate sets are defined using operator constants found in
    the `logical <https://pypi.org/project/logical/>`_ library).

    +------------+-------------+-----------------------------+----------------------------+
    | **inputs** | **outputs** | **operators**               | **minimize**               |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 1          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 2          | 2           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``{id_, not_, and_, or_}``  | ``{id_, not_, and_, or_}`` |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``{id_, not_, and_, xor_}`` | ``{and_}``                 |
    +------------+-------------+-----------------------------+----------------------------+
    | 3          | 1           | ``every``                   | ``every``                  |
    +------------+-------------+-----------------------------+----------------------------+

    The database supports retrieval using index notation, as well.

    >>> circuitdb[1][1][frozenset(logical.every)][frozenset(logical.every)][(0, 0)]
    [((0, 1),), ((0, 0), 0), ((0, 1), 1)]
    >>> circuitdb[1][1][frozenset(logical.every)][frozenset(logical.every)][((0,), (0,))]
    [((0, 1),), ((0, 0), 0), ((0, 1), 1)]

    The top-level database instance has keys that represent to the number of
    inputs of the logical function. The second level down, the keys represent
    the number of outputs of a logical function. The third level down, keys
    represent the set of unary or binary gates to which circuits are restricted.
    Finally, the last level down, the keys represent logical functions.

    >>> list(sorted(list(circuitdb.keys()))) == [1, 2, 3]
    True
    >>> ks = list(sorted(list(circuitdb[1][1].keys())))
    >>> ks[0] == frozenset({logical.and_, logical.or_, logical.not_, logical.id_})
    True
    >>> circuitdb[2][1][ks[0]][ks[0]][(1,1,1,1)]
    [((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 1, 1, 1), 0, 2), ((0, 1), 3)]

    Note that the internal representation organizes the circuits by arity.

    >>> _d = {i: _db._data[i][1] for i in range(1,4)}
    >>> all(len(_d[1][o][m].keys()) == 4 for o in _d[1] for m in _d[1][o])
    True
    >>> all(len(_d[2][o][m].keys()) == 16 for o in _d[2] for m in _d[2][o])
    True
    >>> all(len(_d[3][o][m].keys()) == 256 for o in _d[3] for m in _d[3][o])
    True
    """
    def __call__(self, truthtable, operators=None, minimize=None):
        """
        Function-like interface for the circuit database, with user-friendly
        defaults for retrieving circuit data.

        By supplying a logical function (represented as a tuple), it is possible
        to retrieve a smallest circuit that implements that function. Logical
        functions having one output are represented using a tuple of
        integers (or booleans), or a tuple of one-element tuples.

        >>> circuitdb((0, 0))
        [((0, 1),), ((0, 0), 0), ((0, 1), 1)]
        >>> circuitdb(((0,), (0,)))
        [((0, 1),), ((0, 0), 0), ((0, 1), 1)]
        >>> circuitdb((False, False))
        [((0, 1),), ((0, 0), 0), ((0, 1), 1)]

        A logical function having a vector of two outputs is represented using
        a tuple of two-element tuples.

        >>> circuitdb(((1, 0), (1, 0), (1, 0), (0, 1)))
        [0, 1, ((0, 0, 0, 1), 0, 1), ((1, 0), 2), ((0, 1), 3), ((0, 1), 2)]

        It is also possible to retrieve a smallest circuit that only uses gates
        from a specific set of gates.

        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [logical.id_, logical.not_, logical.and_, logical.or_])
        [((0, 1),), ((0, 1),), ((0, 1),), ((1, 0), 0), ((0, 0, 0, 1), 0, 3), ((0, 1), 4)]

        Any attempt to access the data with a malformed key raises an
        exception.

        >>> circuitdb([0, 0, 0, 0])
        Traceback (most recent call last):
          ...
        TypeError: truth table must be a tuple
        >>> circuitdb((0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: truth table must have a length that is a power of two
        >>> circuitdb(('abc', 'xyz'))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range [0, 1], or tuples of such
        >>> circuitdb((('abc', 'xyz')))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range [0, 1], or tuples of such
        >>> circuitdb(((1, 'abc'), (1, 0), (1, 0), (0, 1)))
        Traceback (most recent call last):
          ...
        TypeError: truth table must contain boolean values, integers in the range [0, 1], or tuples of such
        >>> circuitdb(((), ()))
        Traceback (most recent call last):
          ...
        ValueError: truth table entries must each represent at least one value
        >>> circuitdb(((), (1, 0)))
        Traceback (most recent call last):
          ...
        ValueError: truth table entries must all have the same length
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 4
        >>> circuitdb(((0,0,0), (1,1,1)))
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 1 having output vectors of length 1
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), 132)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [(0, 1, 0)])
        Traceback (most recent call last):
          ...
        ValueError: collection of operators must only contain valid operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), [(0, 1)])
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 that have only the specified operators
        >>> id_not_and_or = [logical.id_, logical.not_, logical.and_, logical.or_]
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, 123)
        Traceback (most recent call last):
          ...
        TypeError: collection of operators the number of which to minimize must be a set, frozenset, list, or tuple
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, [(0, 1, 0)])
        Traceback (most recent call last):
          ...
        ValueError: collection of operators the number of which to minimize must contain only valid operators
        >>> circuitdb((0, 0, 0, 0, 0, 0, 0, 0), id_not_and_or, [(0, 1)])
        Traceback (most recent call last):
          ...
        ValueError: no entries for functions of arity 3 for specified operators and minimization criteria

        Additional exhaustive tests are presented below.

        >>> from itertools import product
        >>> def eval(c, v):
        ...     m = list(v)
        ...     for e in c[len(m):]:
        ...         m.append(e[0](*[m[e[i]] for i in range(1, len(e))]))
        ...     return m[-1]
        >>> evals = lambda c, a: tuple([eval(c, v) for v in product(*[[0, 1]]*a)])
        >>> _d = {i: _db._data[i][1] for i in range(1,4)}
        >>> aoms = [(a, o, m) for a in _d for o in _d[a] for m in _d[a][o]]
        >>> all(all(t == evals(circuitdb(t, o, m), a) for t in product(*[[0, 1]]*(2**a))) for (a, o, m) in aoms)
        True
        >>> def eval(c, v):
        ...     m = list(v)
        ...     for e in c[len(m):]:
        ...         m.append(e[0](*[m[e[i]] for i in range(1, len(e))]))
        ...     return tuple(m[-2:])
        >>> evals = lambda c, a: tuple([eval(c, v) for v in product(*[[0, 1]]*a)])
        >>> aoms = [(a, o, m) for a in [2] for o in _db._data[a][2] for m in _db._data[a][2][o]]
        >>> pairs = [(0, 0), (0, 1), (1, 0), (0, 1)]
        >>> all(all(t == evals(circuitdb(t, o, m), a) for t in product(*[pairs]*(2**a))) for (a, o, m) in aoms)
        True
        """
        # Ensure the function truth table is a tuple.
        if not isinstance(truthtable, tuple):
            raise TypeError('truth table must be a tuple')

        # Ensure that the function truth table has valid entry types.
        if all(isinstance(e, tuple) for e in truthtable):
            if not all(all(b in [0, 1, False, True] for b in e) for e in truthtable):
                raise TypeError('truth table must contain boolean values, integers in the range [0, 1], or tuples of such')
        elif not all(e in [0, 1, False, True] for e in truthtable):
            raise TypeError('truth table must contain boolean values, integers in the range [0, 1], or tuples of such')

        # Determine the arity of the function represented by the truth table.
        arity = int(math.log2(len(truthtable)))

        # Check that the number of entries in the truth table is a power of two.
        if len(truthtable) < 1 or 2**arity != len(truthtable):
            raise ValueError('truth table must have a length that is a power of two')

        # Determine the number of outputs in the truth table (and check it is consistent).
        coarity = 1
        if all(isinstance(e, tuple) for e in truthtable):
            ls = set(len(e) for e in truthtable)
            if len(ls) == 1:
                coarity = list(ls)[0]
                if coarity < 1:
                    raise ValueError('truth table entries must each represent at least one value')
                elif coarity == 1: # Convert tuple of singleton tuples into simple tuple.
                    truthtable = tuple(e[0] for e in truthtable)
            else:
                raise ValueError('truth table entries must all have the same length')

        # Ensure that data for functions of the requested arity and coarity is available.
        if arity not in _db._data:
            raise ValueError('no entries for functions of arity ' + str(arity))

        if coarity not in _db._data[arity]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +\
                'having output vectors of length ' + str(arity)
            )

        # Normalize the truth table representation.
        if coarity == 1:
            truthtable = tuple(map(int, truthtable))
        else:
            truthtable = tuple(tuple(map(int, e)) for e in truthtable)

        # Allow all operators by default or check that data is present for given operators.
        operators = frozenset(logical.every) if operators is None else operators

        if not isinstance(operators, (set, frozenset, list, tuple)):
            raise TypeError('collection of operators must be a set, frozenset, list, or tuple')

        if not frozenset(operators).issubset(logical.every):
            raise ValueError('collection of operators must only contain valid operators')

        if frozenset(operators) not in _db._data[arity][1]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +\
                'that have only the specified operators'
            )

        # Minimize the total number of operators of any available kind by default.
        minimize_ = list(sorted(list(_db._data[arity][1][frozenset(operators)].keys())))[0]
        minimize = minimize_ if minimize is None else minimize

        # Check that the operators to minimize are valid and corresponding data exists.
        if not isinstance(minimize, (set, frozenset, list, tuple)):
            raise TypeError(
                'collection of operators the number of which to minimize ' +\
                'must be a set, frozenset, list, or tuple'
            )

        if not frozenset(minimize).issubset(logical.every):
            raise ValueError(
                'collection of operators the number of which to minimize ' +\
                'must contain only valid operators'
            )

        if frozenset(minimize) not in _db._data[arity][1][frozenset(operators)]:
            raise ValueError(
                'no entries for functions of arity ' + str(arity) + ' ' +\
                'for specified operators and minimization criteria'
            )

        # Wrapping result in list constructor ensures that users do not inadvertently
        # modify the data set entries.
        return list(_db._data[arity][coarity][frozenset(operators)][frozenset(minimize)][truthtable])

# Exported object with function-like and dictionary-like interfaces
# hides the class definition that is used to construct it.
if os.environ.get("CIRCUITDB_DOCS") != "1":
    circuitdb_ = circuitdb
    circuitdb = circuitdb_(_db._data)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
