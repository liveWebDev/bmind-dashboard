"""
bMind
Package for dealing with tokenize for all the things.
"""
from nltk.tokenize import TreebankWordTokenizer

'''
Return a list of word tokens tokenized based on Treebank Word Tokenizer 
'''


def word_tokenize(sentence):
    word_tokenizer = TreebankWordTokenizer()
    return word_tokenizer.tokenize(sentence)
