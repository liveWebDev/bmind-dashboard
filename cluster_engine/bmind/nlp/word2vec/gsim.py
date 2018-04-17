import difflib
import re
import warnings

import numpy as np
from gensim.models import Word2Vec

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

model = Word2Vec()


def create_model(corpus):
    model = Word2Vec(corpus, size=100, window=5, min_count=3, workers=8)
    return model


def save_model(filepath, filename):
    model.save(filepath + filename)


def load_model(filepath, filename):
    global model
    model = Word2Vec.load(filepath + filename)
    return model


def get_relative_words_all(word):
    word_ini = word
    i = 0
    words = list()
    words.append(word)
    while i < len(words) and i <= 10:
        [words.append(w) for w in get_relative_words(words[i]) if w not in words]

        i += 1

    words.remove(word_ini)
    return words


def get_relative_bi_all(word):
    word_ini = word
    i = 0
    words = list()
    words.append(word)
    while i < len(words) and i <= 10:
        [words.append(w) for w in get_relative_bi(words[i]) if w not in words]

        i += 1

    words.remove(word_ini)
    return words


def get_relative_words(word, tolerance=0.75):
    if word in model.wv.vocab:
        # word = 'profunda'

        # word_sims = model.similar_by_word(word,topn=100)
        word_sims = [(k, v) for k, v in model.similar_by_word(word, topn=50) if v >= tolerance]
        # relative = difflib.get_close_matches(word, [w for w, s in word_sims[:100] if w[0] == word[0]], cutoff=0.60)
        # relative = difflib.get_close_matches(word, [w for w, s in word_sims[:300] if w[0] == word[0] and get_dif_bi_letter(word, w) <= 3], cutoff=0.60)

        relative = list()
        for w, s in word_sims:
            if len(word) >= len(w):
                wordref = word
                wordcomp = w
            else:
                wordref = w
                wordcomp = word

            if w[0] == word[0] and get_dif_bi_letter(wordref, wordcomp) <= 1 and not contains_int(w):
                relative.append(w)

        # relative = [w for w, s in word_sims if w[0] == word[0] and get_dif_bi_letter(word, w) <= 1 and not contains_int(w)]

        # print(relative)
        # print(relative_bi)

        return relative
    else:
        return []


def get_relative_words_all_regular(word, remove_alphanum=True):
    word_ini = word
    i = 0
    words = []
    words.append(word)
    while i < len(words) and i <= 10:
        # print(words)
        # print(words[i])
        [words.append(w) for w in get_relative_words_regular(words[i]) if w not in words
         and (remove_alphanum and not contains_int(w))]
        i += 1

    words.remove(word_ini)
    return words


def get_relative_words_regular(word):
    fl = word[0]
    if word in model.wv.vocab:
        relative = difflib.get_close_matches(word, [w for w, s in model.similar_by_word(word)], cutoff=0.60)
        relative = [r for r in relative if r[0] == fl]  # tolera resultados com letra inicial igual
        return relative
    else:
        return []


# [w for w, s in dp.model.similar_by_word(word,topn=400) if w[0] == word[0] and get_dif_bi_letter(word, w) <= 1]
def get_dif_bi_letter(word, wordcompare):
    diflen = len(set(re.findall(r'(?=([a-zA-Z]{2}))', wordcompare)) - set(re.findall(r'(?=([a-zA-Z]{2}))', word)))
    return diflen


def get_dif_tri_letter(word, wordcompare):
    diflen = len(set(re.findall(r'(?=([a-zA-Z]{3}))', wordcompare)) - set(re.findall(r'(?=([a-zA-Z]{3}))', word)))
    return diflen


# TODO passar para util
def contains_int(text):
    re_d = re.compile('\d')
    return True if re_d.search(text) != None else False


def get_sim_bi_letter(word, wordcompare, gram=2):
    w = re.findall(r'(?=([a-zA-Z]{%s}))' % gram, word)
    wc = re.findall(r'(?=([a-zA-Z]{%s}))' % gram, wordcompare)

    pairs_len = max([len(w), len(wc)])

    score_max = sum([np.exp(1 * (pairs_len - i)) for i in range(pairs_len)])

    sim = [(ix, i) if i == j else (ix, '') for ix, (i, j) in enumerate(zip(w, wc))]
    score = sum([np.exp(1 * (pairs_len - i)) * (-1 if w == '' else 1) for i, w in sim])

    return 0 if score_max == 0 else score / score_max


def get_relative_bi(word, cutoff=0.60):
    if word in model.wv.vocab:
        sims = [(w, get_sim_bi_letter(word, w)) for w, s in model.similar_by_word(word, 100)]
        sims = [w for w, v in sims if v >= cutoff]
        return sims
    else:
        return []
