__all__ = [
    "weighted_sum",
    "choquet_integral_capacity",
    "choquet_integral_mobius",
]

from typing import List, cast

from ..core.aliases import (
    NumericPerformanceTable,
    NumericValue,
    PerformanceTable,
)
from ..core.performance_table import (
    apply_criteria_weights,
    normalize,
    sum_table,
)
from ..core.scales import Scale
from ..core.sets import difference, index_to_set
from ..core.sorting import sort_elements_by_values


def normalized_weighted_sum(
    performance_table: NumericPerformanceTable,
    criteria_weights: List[NumericValue],
) -> List[NumericValue]:
    """Compute alternatives values as weighted sum of normalized alternatives'
    performances.

    :param performance_table:
    :param criteria_weights:
    :return: alternatives values
    """
    weighted_table = cast(
        PerformanceTable,
        apply_criteria_weights(performance_table, criteria_weights),
    )
    res = sum_table(weighted_table, axis=1)
    res = cast(List[NumericValue], res)
    return res


def weighted_sum(
    performance_table: PerformanceTable,
    criteria_scales: List[Scale],
    criteria_weights: List[NumericValue],
) -> List[NumericValue]:
    """Compute alternatives values as weighted sum of alternatives'
    performances.

    :param performance_table:
    :param criteria_scales:
    :param criteria_weights:
    :return: alternatives values
    """
    normalized_table = normalize(performance_table, criteria_scales)
    weighted_table = cast(
        PerformanceTable,
        apply_criteria_weights(normalized_table, criteria_weights),
    )
    res = sum_table(weighted_table, axis=1)
    res = cast(List[NumericValue], res)
    return res


def choquet_integral_capacity(
    values: List[NumericValue], capacity: List[NumericValue]
) -> NumericValue:
    """Return Choquet integral using a capacity.

    :param values:
    :param capacity:
    :return:

    .. note:: Implementation is based on [2]_.
    """
    permutation = [*range(len(values))]
    sort_elements_by_values(values, permutation, reverse=True)
    index = len(capacity) - 1
    res = 0
    for i in permutation:
        next_index = difference(index, 2 ** i)
        res += values[i] * (capacity[index] - capacity[next_index])
        index = next_index
    return res


def choquet_integral_mobius(
    values: List[NumericValue], mobius: List[NumericValue]
) -> NumericValue:
    """Return Choquet integral using a möbius.

    :param values:
    :param mobius:
    :return:

    .. note:: Implementation is based on [2]_.
    """
    return sum(
        mobius[t] * min(index_to_set(t, values)) for t in range(1, len(mobius))
    )
