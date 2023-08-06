"""
Модуль для реализации алгоритма бинарного поиска.

Болдырев Владимир
vladimir.boldyrev.2003@mail.ru

Используется для поиска позиции искомого элемента в списке,
полученном в модуле input_data.

Ф-я binary_search - реализация алгоритма
"""

def binary_search(source: list, val: int) -> int:
    """Return index of val element in source.

    Keyword arguments:
    source -- the sorted list
    val -- the sought-for value

    >>> binary_search([7, 34, 55, 77, 87, 95, 102], 55)
    2
    >>> binary_search([2, 5, 9, 10, 16, 50, 87, 135, 200], 50)
    5
    """
    first = 0
    last = len(source)-1
    index = None
    while (first <= last) and (index is None):
        mid = (first+last)//2
        if source[mid] == val:
            index = mid
        else:
            if val < source[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return index