"""
А.О. Блинов,КИ21-16/1Б, вариант 3
Программа реализующая выборочную сортировку
"""


def check_list(base_list):
    """
    Функция для проверки списка на корректность данных

    >>> check_list()
    TypeError
    >>> check_list(1,'a',2)
    TypeError
    """
    if not base_list:
        raise TypeError('Введён некорректный список')
    for i in base_list:
        if not str(i).isdigit():
            if not str(i)[1:].isdigit():
                raise TypeError('Введён некорректный список')


def selection_sort_1(base_list):
    """
    Выборочная сортировка по возрастанию

    >>> selection_sort_1([5, 2, 4, 3])
    [2, 3, 4, 5]
    >>> selection_sort_1([7, 6, 4, 2])
    [2, 4, 6, 7]
    """
    check_list(base_list)
    for i in range(len(base_list) - 1):
        minimal = i
        for j in range(i + 1, len(base_list)):
            if base_list[j] < base_list[minimal]:
                minimal = j
        base_list[i], base_list[minimal] = base_list[minimal], base_list[i]
    return base_list


def selection_sort_2(base_list):
    """
    Выборочная сортировка по убыванию

    >>> selection_sort_2([5, 2, 4, 3])
    [5, 4, 3, 2]
    >>> selection_sort_2([7, 6, 4, 2])
    [7, 6, 4, 2]
    """
    check_list(base_list)
    for i in range(len(base_list) - 1):
        maximum = i
        for j in range(i + 1, len(base_list)):
            if base_list[j] > base_list[maximum]:
                maximum = j
        base_list[i], base_list[maximum] = base_list[maximum], base_list[i]
    return base_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
