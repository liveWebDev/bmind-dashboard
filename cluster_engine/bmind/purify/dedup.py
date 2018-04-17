import codecs
import datetime
import importlib.util
import itertools
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("cleaning", BASE_DIR + "/nlp/cleaning.py")
cleaning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleaning)

spec2 = importlib.util.spec_from_file_location("tokenize", BASE_DIR + "/nlp/tokenize.py")
tokenize = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(tokenize)

spec3 = importlib.util.spec_from_file_location("gsim", BASE_DIR + "/nlp/word2vec/gsim.py")
gsim = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(gsim)


class Dedup:

    def __init__(self, model, projectpath='', modelpath=''):
        self.projectpath = projectpath
        self.modelpath = modelpath
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.ambiguous_words = self.read_ambiguous_words()
        self.synonyms_words = self.read_synonyms_words()
        self.read_colors = self.read_colors()
        self.read_fruits = self.read_fruits()
        # self.model = gsim.load_model(projectpath, modelpath)
        self.model = model
        self.relative_words = dict()
        self.relative_words_aux = dict()

    def read_ambiguous_words(self):
        return codecs.open(os.path.abspath(self.here + '/dedup/ambiguous.txt'), 'r',
                           encoding='utf-8').read().splitlines()

    def read_synonyms_words(self):
        s = codecs.open(os.path.abspath(self.here + '/dedup/synonyms.json'), 'r', encoding='utf-8').read()
        return eval(s)

    def read_colors(self):
        s = codecs.open(os.path.abspath(self.here + '/dedup/cores.txt'), 'r', encoding='utf-8').read().splitlines()
        return s

    def read_fruits(self):
        s = codecs.open(os.path.abspath(self.here + '/dedup/frutas.txt'), 'r', encoding='utf-8').read().splitlines()
        return s

    def solve_ambiguous(self, text):
        '''Read from ambiguous words list file'''

        for word in self.ambiguous_words:
            text = text.replace(word, '1_' + word)

        return text

    def solve_synonyms(self, text):

        for n, word in enumerate(text):
            if word in self.synonyms_words:
                text[n] = self.synonyms_words.get(word)

        return text

    def create_relative_dict_xxx(self, text, irec=1):
        if irec % 1000 == 0:
            print("{} | {}".format(str(datetime.datetime.now()), irec))

        text = cleaning.sentence_clean(text)
        text = self.solve_ambiguous(text)
        text = tokenize.word_tokenize(text)
        text = self.solve_synonyms(text)

        text_1 = {w: (gsim.get_relative_words_all(w)) for w in text
                  if not cleaning.contains_int(w)
                  # if len(w) >= 3	and not cleaning.contains_int(w)
                  and w not in self.relative_words
                  }

        text_2 = {w: (gsim.get_relative_words_all_regular(w)) for w in text
                  if not cleaning.contains_int(w)
                  and w not in self.relative_words
                  }

        text_3 = {w: gsim.get_relative_bi_all(w) for w in text
                  if not cleaning.contains_int(w)
                  and w not in self.relative_words
                  }

        dicts = [text_1, text_2, text_3]
        super_dict = {}

        for d in dicts:
            for k, v in d.items():
                super_dict.setdefault(k, []).append(v)

        for k, v in super_dict.items():
            super_dict[k] = list(set(itertools.chain(*v)))

        self.relative_words.update(super_dict)

    def create_relative_dict(self, text, irec=1):
        if irec % 1000 == 0:
            print("{} | {}".format(str(datetime.datetime.now()), irec))

        text = cleaning.sentence_clean(text)
        text = self.solve_ambiguous(text)
        text = tokenize.word_tokenize(text)
        text = self.solve_synonyms(text)

        text_relative_reg = {w: (gsim.get_relative_words_all_regular(w)) for w in text
                             if not cleaning.contains_int(w)
                             and w not in self.relative_words}

        text_relative = {w: (gsim.get_relative_words_all(w)) for w in text
                         if not cleaning.contains_int(w)
                         # if len(w) >= 3	and not cleaning.contains_int(w)
                         and w not in self.relative_words}

        text_relative_reg.update(text_relative)

        self.relative_words.update(text_relative_reg)

    def create_relative_dict_regular(self, text, irec=1):
        if irec % 1000 == 0:
            print("{} | {}".format(str(datetime.datetime.now()), irec))

        text = cleaning.sentence_clean(text)
        text = self.solve_ambiguous(text)
        text = tokenize.word_tokenize(text)

        text_relative = {w: (gsim.get_relative_words_all_regular(w)) for w in text
                         if not cleaning.contains_int(w)
                         and w not in self.relative_words}

        self.relative_words.update(text_relative)

    def update_dict(self):
        universal_dict = self.relative_words

        all_words = [[i for i in v] for k, v in universal_dict.items()]
        all_words = list(set(itertools.chain(*all_words)))

        for key_word in all_words:
            final_items = list()
            for k, v in universal_dict.items():
                if key_word in v:
                    for item in v:
                        final_items.append(k)
                        final_items.append(item)
            final_items = list(set(final_items))
            universal_dict.update({key_word: final_items})

        # Remove dedundance between in key and value element
        for k, v in universal_dict.items():
            if k in v:
                v.remove(k)

    def to_cluster(self, text, remove_num=False, irec=1):
        if irec % 1000 == 0:
            print("{} | {}".format(str(datetime.datetime.now()), irec))

        text = cleaning.sentence_clean(text)
        text = self.solve_ambiguous(text)
        text = tokenize.word_tokenize(text)
        text = self.solve_synonyms(text)

        if (remove_num):
            text_relative = {w: self.relative_words[w] for w in text
                             if w in self.relative_words and len(self.relative_words[w]) > 0
                             and not cleaning.contains_int(w)}
        else:
            text_relative = {w: self.relative_words[w] for w in text
                             if w in self.relative_words and len(self.relative_words[w]) > 0}

        # for w, r in self.relative_words.items():
        for w, r in text_relative.items():
            for v in r:
                text.insert(0, v)

        # THIS IS THE MOMENT!
        text = hash(''.join(sorted(set(text))))

        return text

    def to_cluster_literal(self, text, irec=1, sep=''):
        if irec % 1000 == 0:
            print("{} | {}".format(str(datetime.datetime.now()), irec))

        text = cleaning.sentence_clean(text, remove_num=True)
        text = self.solve_ambiguous(text)
        text = tokenize.word_tokenize(text)
        text = self.solve_synonyms(text)

        text_relative = {w: self.relative_words[w] for w in text
                         if w in self.relative_words and len(self.relative_words[w]) > 0}

        # for w, r in self.relative_words.items():
        for w, r in text_relative.items():
            for v in r:
                text.insert(0, v)

        text = sep.join(sorted(set(text)))

        return text

    # UTIL

    def set_row_index(self, row):
        return row.name

    # df['rowIndex'] = df.apply(rowIndex, axis=1)

    def reg_encode(self, row):
        return row.encode('latin-1').decode('utf-8').upper()

    def norm(self, row):
        return normalize('NFKD', row).encode('ASCII', 'ignore').decode('ASCII')

    def get_relative(self, word, tolerance=0.75):
        relative = difflib.get_close_matches(word, [w for w, s in model.similar_by_word(word)], cutoff=0.60)
        word_sims = [(k, v) for k, v in model.similar_by_word(word, topn=50) if v >= tolerance]

        relativelist = list()
        for w, s in word_sims:
            if len(word) >= len(w):
                wordref = word
                wordcomp = w
            else:
                wordref = w
                wordcomp = word

            if w[0] == word[0] and get_dif_bi_letter(wordref, wordcomp) <= 1 and not contains_int(w):
                relativelist.append(w)

        return {"relative": relative, "word_sims": word_sims.keys}

    def set_row_main(self, df):
        df['ROW_MAIN'] = df.groupby(['CLUSTER_ID']).cumcount()+1
        df['ROW_MAIN'] = df.apply(lambda row: 1 if row['ROW_MAIN'] == 1 else 0, axis=1) 

        return df