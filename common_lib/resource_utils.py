import random


def random_file_name(name):
    suffix = name.split('.')[-1]
    rand_str = '123456789abcdefghijklmnopqrstuvwxyz'
    length = len(rand_str)
    file_name = ''
    for i in range(0, 20):
        char = rand_str[random.randint(0, length - 1)]
        file_name = file_name + char

    return file_name + '.' + suffix