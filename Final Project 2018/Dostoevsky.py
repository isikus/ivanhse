import re
import os
import json

from random import uniform
from train import train
from ast import literal_eval

def generate_sentence(model,word):
    phrase = ''
    t0, t1 = '$', word
    while 1:
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
        t0, t1 = t1, unirand(model[t0, t1])
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

def generate_answer(w):
    if not os.path.exists('model_corpus.json'):
        m = train('corpus.txt')
    else:
        with open('model_corpus.json','r',encoding='utf-8') as injson:
            obj = json.load(injson)
            m = {literal_eval(k):v for k, v in obj.items()}
    answer = generate_sentence(m,w)
