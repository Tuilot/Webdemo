import random
from article.models import Article


def create_article_id():
    seq = 'abcdefghijklmnopqrstuvwxyz123456789'
    new_id = ''
    while new_id == '':
        for i in range(0, 10):
            if i == 0:
                char = random.choice(seq)
                new_id = new_id + str(char)
            else:
                char = random.choice(seq)
                new_id = new_id + str(char)
        if len(Article.objects.filter(id__exact=new_id)) > 0:
            new_id = ''
    return new_id
