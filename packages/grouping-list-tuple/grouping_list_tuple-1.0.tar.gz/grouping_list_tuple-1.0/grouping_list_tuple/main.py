import group
from random_list import random_list
import argparse
import doctest
import pytest

parser = argparse.ArgumentParser(description="Консольное меню")
parser.add_argument("-m", "--mode", help="Выберите режим работы: start - запуск программы; "
                                         "pytest - вывод тестов pytest; doctest - вывод тестов doctest.",
                    choices=["start", "pytest", "doctest"], default="start")
args = parser.parse_args()


def main(mode):
    """Варианты запуска"""
    if mode == "start":
        start()
    elif mode == "pytest":
        pytest.main(['-v'])
    elif mode == "doctest":
        doctest.testmod(group, verbose=True)


def start():
    """Обычное меню"""
    while (menu := input("1 - Сгенерировать массив с значениями \n"
                         "2 - Сгенерировать массив с кортежами \n"
                         "3 - Выход из программы \n")) != '3':
        if menu == '1':
            print(group.grouping(random_list(menu), menu))
        elif menu == '2':
            massif = random_list(menu)
            choice = input("Надо указать элемент по которому будет группировка? yes or no ")
            while choice not in ('yes', 'no'):
                choice = input("yes or no ")
            if choice == 'no':
                print(group.grouping(massif, menu))
            else:
                sort = input("Укажите индекс элемента кортежа который будет ключом сортировки: ")
                while type(sort) is str:
                    try:
                        sort = int(sort)
                        print(group.grouping(massif, menu, sort))
                    except (ValueError, IndexError):
                        sort = input("Неверное значение ")


if __name__ == '__main__':
    main(args.mode)
