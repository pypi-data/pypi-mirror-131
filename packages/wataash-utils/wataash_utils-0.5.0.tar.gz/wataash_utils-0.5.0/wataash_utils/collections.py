# SPDX-License-Identifier: Apache-2.0

import functools
import typing as t

_T = t.TypeVar('_T')


def sets_union(sets: t.Iterable[set[t.Generic[_T]]]) -> set[_T]:
    """
    >>> sets_union([{0, 1}, {1, 2}])
    {0, 1, 2}
    """
    return functools.reduce(lambda set_accum, set_new: set_accum | set_new, sets)


def sets_intersection(sets: t.Iterable[set[_T]]) -> set[_T]:
    """
    >>> sets_intersection([{0, 1}, {1, 2}])
    {1}
    """
    return functools.reduce(lambda set_accum, set_new: set_accum & set_new, sets)
