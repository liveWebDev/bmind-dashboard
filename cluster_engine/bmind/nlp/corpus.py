import string

from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

stopset = set(stopwords.words('portuguese')) | set(string.punctuation)
stopset_exception = ['ele', 'ela', 'sem', 'com']
stopset = list(set(stopset).difference(set(stopset_exception)))


def read_corpus_from_txt(directorypath, filepattern):
    corpus_reader = PlaintextCorpusReader(directorypath, filepattern, encoding='utf-8')
    corpus_raw = corpus_reader.raw().replace('\r\n', '.\r\n')
    return corpus_raw
