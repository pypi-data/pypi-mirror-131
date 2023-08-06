"""
Модуль для ввода и проверки итерируемого объекта
"""


import ast


def input_iterable():
    """
    Функция для ввода итерируемого объекта

    :return: Итерируемый объект
    """
    iterable = input('Введите итерируемый объект ')
    while not check_iterable(iterable):
        iterable = input('Введите итерируемый объект ')
    return ast.literal_eval(iterable)


def check_iterable(iterable):
    """
    Функция для проверки введенного итерируемого объекта

    :param iterable: Итерируемый объект
    :return: True or False
    """
    try:
        iter(ast.literal_eval(iterable))
    except (TypeError, ValueError, SyntaxError):
        return False
    return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()
