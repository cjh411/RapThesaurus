# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:32:26 2017

@author: christopherhedenberg
"""

import pandas as pd
from gensim import corpora
import gensim
from collections import defaultdict
from gensim.models.doc2vec import LabeledSentence
from gensim import utils
import gensim
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import pickle


size=50
mdlds = pd.read_csv("/Output/MasterDatasetYear.csv")
lyrics = mdlds['lyrics'].tolist()
spellcheck = pd.read_csv("/Output/MisspellingsCleaned/Sheet 3-Table 1.csv")
lookup = spellcheck['Word'].tolist()
correct = spellcheck["Correct"].tolist()
artists=mdlds['artist'].tolist()
artists=[unicode(x) for x in artists]
years = mdlds['year'].tolist()




spelling_dict={}
i=0
for word in lookup:
    spelling_dict[word] = correct[i]
    i+=1

stopwords = []
lyrics = [[x.decode('utf8').encode('ascii', errors='ignore').replace("'","") for x in lyric.lower().split() if x not in stopwords] for lyric in lyrics]

frequency = defaultdict(float)
for text in lyrics:
    for token in text:
        frequency[token] += 1



texts = [[token for token in lyric if frequency[token] > 10] for lyric in lyrics]
texts_clnd = []
artists_clnd = []
year_clnd = []
for i in range(len(texts)):
    if len(texts)>1:
        texts_clnd.append(texts[i])
        artists_clnd.append(artists[i])
        year_clnd.append(years[i])
        



phrases = gensim.models.phrases.Phrases(texts_clnd,min_count=25)
bigram = gensim.models.phrases.Phraser(phrases)
bigram_text = [bigram[item] for item in texts_clnd]

freq_lookup ={}
for text in bigram_text:
    for token in text:
        freq_lookup[token] = token

for i in range(len(lookup)):
    freq_lookup[lookup[i]]=correct[i]

bigram_text = [[freq_lookup[item] for item in verse] for verse in bigram_text]





sentences = []
for i in range(len(bigram_text)):
    sentences.append(LabeledSentence(bigram_text[i],[artists_clnd[i]]))

model = gensim.models.Doc2Vec(sentences,min_count=10,size=size,workers=4,window=8,dbow_words=1)
model.save("/Modeling/Doc2VecFinalModel.bin")

