#!/usr/bin/env python

import argparse
import gensim
import re

def tokenizer(raw_doc):
    '''Tokenize a raw document string to list of list of words.
    
    Example:
        > s = "Nonsense?  kiss off, geek. what I said is true.  I'll have your account terminated."
        > tokenizer(s)
        [['nonsense'],
         ['kiss', 'off', 'geek'],
         ['what', 'i', 'said', 'is', 'true'],
         ['ill', 'have', 'your', 'account', 'terminated']]
        
    '''
    sentences = re.findall(r'(?ms)\s*(.*?(?:\.|\?|!))', raw_doc)
    sentences = map(lambda s : s.split(), sentences)
    remove_non_alpha = re.compile('[^a-zA-Z0-9]')
    for i, s in enumerate(sentences):
        sentences[i] = map(lambda w : remove_non_alpha.sub('', w), s)
        sentences[i] = map(lambda w : w.lower(), sentences[i])
    return sentences

def main(args):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Train a doc2vec classifier'
    )
    parser.add_argument(
        '--df', metavar = '...', type = str, nargs = '+',
        help = 'List of pandas data frames'
    )
    parser.add_argument(
        '--label', type = str, help = 'Label to extract from data frames'
    )
    parser.add_argument(
        '--output', type = str
    )

    args = parser.parse_args()
    main(args)