def input_k():
    """
    Функция для ввода числа элементов

    :return: Целое число элементов
    """
    k = input('Введите число элементов, выбираемых из итерируемого объекта ')
    while not check_k(k):
        k = input('Введите число элементов еще раз ')
    return int(k)


def check_k(k):
    """
    Функция для проверки введенного числа элементов

    :param k: Число элементов, выбираемых из итерируемого объекта
    :return: True or False

    """
    try:
        int(k)
    except (TypeError, ValueError, SyntaxError):
        return False
    return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()
