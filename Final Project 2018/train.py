import re
import json
from collections import defaultdict

r_alphabet = re.compile(u'[а-яёА-ЯЁa-zA-Z0-9-]+|[.,:;?!]+')

def gen_lines(corpus):
    data = open(corpus,'r',encoding='utf-8')
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    
    with open('model_'+re.sub('txt','json',corpus), 'w', encoding='utf-8') as outfile:
        json.dump({str(k):v for k, v in model.items()}, outfile, ensure_ascii = False)
    return model

