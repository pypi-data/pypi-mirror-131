"""
Основной модуль пакета, выступакет в роли точки входа

Болдырев Владимир
vladimir.boldyrev.2003@mail.ru

Ф-я execution - повторный ввод с возможностью завершения,
и вывода соответствующей информации в случае некоректного ввода
Ф-я main - командный линейный интерфейс (выбор режима запуска)
"""
import click
import pytest
import doctest
from input_verification import input_validation
from binary_search_algorithm import binary_search

def menu_extraction(menu):
    """Displays main menu of programm."""
    for k, v in menu.items():
        print(f'{k} - {v[0]}')
    print('2 - Завершить программу')

def binary_search_initialization() -> list and int:
    """Take user input and return binary_search func result of it."""
    source, val = input_validation()
    return binary_search(source, val)

def execution():
    """Return result of the programm."""


    menu = {
        '1': ('Задать массив и инициализировать поиск',
              binary_search_initialization),
    }

    menu_extraction(menu)
    while (s := input('Выберите: ')) != '2':
        if s in menu:
            print(menu[s][1]())
            menu_extraction(menu)
        else:
            print('Wrong input')


@click.command()
@click.option(
    "--mode", "-m", help="Выберите режим работы: pytest - вывод тестов pytest; doctest - вывод тестов doctest; "
                         "start - запуск программы", default='start')
def main(mode):
    """
    Функиця для реализации командного интерфейса
    :param mode: str, режим запуска пакета
    """
    if mode == "pytest":
        pytest.main([r"Documents\op6\package\tests\tests_unit.py"])
    elif mode == "doctest":
        doctest.testmod()
    elif mode == "start":
        execution()


if __name__ == "__main__":
    main()
