import doctest
import pytest
from iterable_input import input_iterable
from k_input import input_k
import combinations
import click


def menu():
    """
    Меню программы
    """
    print('1. Найти сочетания без повторений для переданной последовательности ',
          '2. Выйти из программы', sep='\n')
    print()


def start():
    """
    Функция для вывода меню и запуска программы
    """
    flag = 1
    while flag:
        menu()
        item = input('Выберите пункт меню ')
        if item.isdigit() and item == '1' or item == '2':
            if item == '1':
                element = input_iterable()
                number = input_k()
                print(combinations.calculating(element, number))
                print()
            if item == '2':
                flag = 0
        else:
            print('Нет такого пункта меню!')


@click.command()
@click.option("--mode", "-m",
              type=click.Choice(["start", "doctest", "pytest"], case_sensitive=True),
              help="Выберите пункт меню: start - запустить программу;"
              "doctest - вывести тесты doctest; pytest - вывести тесты pytest")
def main(mode: str):
    """
    Интерфейс командной строки с возможностью запуска тестов

    :param mode: Режим запуска пакета
    """
    if mode == 'start':
        start()
    elif mode == 'doctest':
        doctest.testmod(combinations, verbose=True)
    elif mode == 'pytest':
        pytest.main(['-v'])


if __name__ == '__main__':
    main()
