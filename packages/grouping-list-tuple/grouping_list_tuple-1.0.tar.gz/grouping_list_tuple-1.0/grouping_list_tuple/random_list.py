from random import randint


def random_list(menu):
    """Генерация массива с рандомными символами"""
    if menu == '1':
        massif = [chr(randint(65, 90)) for _ in range(randint(4, 10))]
    else:
        massif = [(chr(randint(65, 90)), randint(0, 25), chr(randint(65, 90)))
                  for _ in range(randint(4, 10))]
    print(massif)
    return massif
