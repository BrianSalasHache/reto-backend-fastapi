from math import lcm

from fastapi import APIRouter, Query

router = APIRouter(prefix="/math", tags=["math"])


@router.get("/next/{number}")
def next_integer(number: int) -> int:
    """
    Get the next integer of a given integer.

    Args:

        number (int): Integer number.

    Returns:

        int: The next integer after the given number.
    """
    next_n = number + 1
    return next_n


@router.get("/lcm/")
def least_common_multiple(numbers: list[int] = Query()) -> int:
    """
    Get the least common multiple of a list of integers.

    Args:

        numbers (List[int]): List of integer numbers.

    Returns:

        int: The least common multiple of the input numbers.
    """
    _lcm = lcm(*numbers)
    return _lcm
