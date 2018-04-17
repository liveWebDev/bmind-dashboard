'''Doc String'''

import codecs
import os
import re
from unicodedata import normalize

from nltk.stem import RSLPStemmer

__dir = os.path.abspath(os.path.dirname(__file__))


def read_stopwords():
    s = codecs.open(os.path.abspath(__dir + '/dic/stopwords.txt'), 'r', encoding='utf-8').read()
    return eval(s)


stopset = read_stopwords()


def sentence_clean(txt, remove_num=False, remove_stopwords=True):
    if remove_num:
        txt = re.sub('\d', '', txt)

    # TODO: Load File Replace Rules
    # Commom words, count the words
    txt = txt.replace('-', ' ').replace('&', ' ').replace('.', ' ').replace('/', ' ').replace('\\', ' ').replace(
        ' PCT ', ' ').replace(' PCTE ', ' ').replace(' PACOTE ', ' ')

    txt = re.sub(r'[^\w\s]', '', txt)
    txt = txt.lower().strip()

    if remove_stopwords:
        txt = ' '.join([w for w in txt.split(' ') if not w in stopset])
    txt = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    return txt


def word_stemm(word):
    stemmer = RSLPStemmer()

    try:
        word = stemmer.stem(word)
    except:
        print(word)

    return word


def remove_stopwords(text):
    return ' '.join([w for w in text.split(' ') if not w in stopset])


def split_num_letter(text):
    return re.findall('\d+|\D+', text)


# TODO passar para util
def contains_int(text):
    re_d = re.compile('\d')
    return True if re_d.search(text) != None else False
