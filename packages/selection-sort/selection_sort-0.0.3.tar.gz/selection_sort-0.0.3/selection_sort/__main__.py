"""
sys - для безопасного выхода в случае исключения
click - для запусука модуля через cmd
numpy - для работы с массивами
selection_sort - обработка данных
"""
import sys
import click
import numpy as np
import selection_sort


@click.command()
@click.argument('f_and_list', nargs=-1)
def main(f_and_list):
    """
    Главная функция(?)
    """
    f_and_list = np.array(f_and_list)
    if not f_and_list.size:
        print('Вы ничего не ввели')
        sys.exit(0)
    answer = f_and_list[0]
    check_list = np.array(f_and_list)[1:]
    if not check_list.size:
        print('Вы ввели всего 1 число, нужно минимум 2')
        sys.exit(0)
    try:
        answer = int(answer)
    except ValueError:
        print('Вы не ввели число в начале')
        sys.exit(0)
    try:
        check_list = check_list.astype(int)
    except ValueError:
        print('Вы не ввели числа через пробел')
        sys.exit(0)
    if answer == 1:
        result = selection_sort.selection_sort_1(check_list)
        print(*result)
    if answer == 2:
        result = selection_sort.selection_sort_2(check_list)
        print(*result)


if __name__ == '__main__':
    main()
