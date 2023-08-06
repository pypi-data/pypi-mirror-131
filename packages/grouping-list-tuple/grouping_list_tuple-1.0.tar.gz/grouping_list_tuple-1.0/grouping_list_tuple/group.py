def grouping(massif, menu, sort=99):
    """
    Группировка объектов массива по некоторому ключу
    :param massif: список с значениями
    :param menu: каким вариантом будет группировка
    :param sort: индекс элемента группировки
    :return: список кортежей с ключом группировки

    >>> grouping(['A', 'A', 'B', 'A'], 1, -1)
    [('A', ['A', 'A']), ('B', ['B']), ('A', ['A'])]
    >>> grouping([('B', 16, 'U'), ('R', 12, 'R')], 2, -1)
    [('U', [('B', 16, 'U')]), ('R', [('R', 12, 'R')])]
    """
    prev_item = ''
    res = []
    if menu == '1' or menu == '2' and sort == 99:
        for i in massif:
            if i != prev_item:
                res.append((i, []))
                prev_item = i
            res[-1][1].append(i)
    else:
        for i, _ in enumerate(massif):
            if prev_item != massif[i][sort]:
                res.append((massif[i][sort], []))
                prev_item = massif[i][sort]
            res[-1][1].append(massif[i])
    return res
