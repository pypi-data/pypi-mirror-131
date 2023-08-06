def calculating(element: iter, number: int): 
    """
    Функция, реализующая вычисление сочетаний без повторений для переданной последовательности

    :param element: Итерируемый объект
    :param number: Число элементов, выбираемых из итерируемого объекта
    :return: Список всех кортежей длиной равной k

    >>> calculating((1, 2, 3), 2)
    [(1, 2), (1, 3), (2, 3)]
    >>> calculating('ABCD', 3)
    [('A', 'B', 'C'), ('A', 'B', 'D'), ('A', 'C', 'D'), ('B', 'C', 'D')]
    """
    current = tuple(element)
    if number == 0:
        return [[]]
    result = []
    for i in range(0, len(element)):
        m = current[i]
        removed_m = current[i + 1:]
        for p in calculating(removed_m, number - 1):
            result.append(tuple([m] + [*p]))
    return result
