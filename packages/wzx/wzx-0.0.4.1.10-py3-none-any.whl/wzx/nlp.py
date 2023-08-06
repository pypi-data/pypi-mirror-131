from . import funs
import json, time, os, pickle, random, chardet, re
from tqdm.notebook import tqdm,trange
from collections import defaultdict
import jieba
from collections import Counter

def get_corpus(corpus):
    ret = list()
    if type(corpus) is str:
        ret.append(corpus)
        return ret
    elif type(corpus) is list:
        for i in corpus:
            ret.extend(get_corpus(i))
        return ret
    else:
        return ret


def get_counter(corpus,chinese=False,char=True):
    cl = get_corpus(corpus)
    if char:
        chars = [j for i in cl for j in list(i)]
        if chinese:
            chars = filter(funs.is_chinese,chars)
        return Counter(chars)
    else:
        wds = list()
        for i in trange(len(cl)):
            i_ = cl[i]
            wds.append(list(jieba.cut(i_)))
        wds = get_corpus(wds)
        if chinese:
            wds = filter(funs.all_chinese,wds)
        return Counter(wds)