import hashlib
import random

from account.models import Account


def getNewId():
    new_id = ''
    while new_id == '':
        for i in range(0, 7):
            if i == 0:
                char = random.randint(1, 9)
                new_id = new_id + char.__str__()
            else:
                char = random.randint(0, 9)
                new_id = new_id + char.__str__()
        if len(Account.objects.filter(id=new_id)) > 0:
            new_id = ''
    return new_id


def calc_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    return md5_obj.hexdigest()


def random_avatar_name(name):
    suffix = name.split('.')[-1]
    rand_str = '123456789abcdefghijklmnopqrstuvwxyz'
    length = len(rand_str)
    avatar_name = ''
    for i in range(0, 20):
        char = rand_str[random.randint(0, length - 1)]
        avatar_name = avatar_name + char
    print(avatar_name)
    return avatar_name + '.' + suffix
