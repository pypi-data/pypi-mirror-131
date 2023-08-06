"""
Модуль для введения данных, на основе которых вычисляется последовательность

Болдырев Владимир
vladimir.boldyrev.2003@mail.ru

Исползуется для получения данных о левой и правой границах последовательности и
максимальном кол-ве чисел

Функция input_validation() - ввод данных
"""


def input_validation() -> list and int:
    """Return formatted variables for binary_search function."""

    def list_sorting(source: list) -> list:
        """Return the sorted received list."""
        source.sort()
        return source
    
    flag = 1
    flag1 = 0
    flag2 = 0
    while flag == 1:
        try:
            source = list(map(int, input("Задайте массив: ").split()))
            val = int(input("Введите значение искомого элемента: "))
        except ValueError:
            print("Wrong input")
            continue
        for i in source:
            if not isinstance(i, int):
                print("Массив должен состоять только из чисел")
                flag1 = 1
                break
        if flag1 == 1:
            continue
        if len(source) == 0:
            print("Введён пустой массив? Что можно в нём искать?")
            continue
        for i in range(len(source)-1):
            if source[i] > source[i+1]:
                if ((choice := input("Массив не отсортирован. "
                                        "Отсортировать?\n1 - Да\n"
                                        "2 - Нет, ввести заного")) == "1"):
                    list_sorting(source)
                else:
                    flag2 = 1
                    break
        if flag2 == 1:
            continue
        flag = 0
    return(source, val)