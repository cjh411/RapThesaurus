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
import nltk

    
mdlds = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/MasterDatasetYear.csv")

lyrics = mdlds['lyrics'].tolist()


stopwords = []
lyrics = [[x.decode('utf8').encode('ascii', errors='ignore').replace("'","") for x in lyric.lower().split() if x not in stopwords] for lyric in lyrics]

#strange_chars =[[x for x in text if "\xe2" in x] for text in lyrics]
#strange_chars = [x for x in strange_chars if len(x)>0]
#strange_dict = defaultdict(int)
#for sent in strange_chars:
#    for char in sent:
#        strange_dict[char]+=1
        
artists=mdlds['artist'].tolist()

artists=[unicode(x) for x in artists]
years = mdlds['year'].tolist()

frequency = defaultdict(int)
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



size=50   
model = gensim.models.Word2Vec(bigram_text,min_count=10,size=size,workers=4,window=8)


vocab = model.wv.vocab
word_sim_dict={}

for word in vocab:
    word_sim_dict[word]=model.wv.most_similar(word,topn=50)
 
misspellings = []   
for word in word_sim_dict.keys():
    for syn in word_sim_dict[word]:
        if (float(nltk.distance.edit_distance(word,syn[0]))/float(max([len(word),1,len(syn[0])])))<.3 and [word,syn[0]] not in misspellings and [syn[0],word] not in misspellings:
            misspellings.append([word,syn[0],0])
  
i=0
for pair in misspellings:
    if (pair[0][len(pair[0])-1]=="s" and pair[0][:len(pair[0])-1]==pair[1]) or (pair[1][len(pair[1])-1]=="s" and pair[1][:len(pair[1])-1]==pair[0]) :
        misspellings[i][2]=1
    elif (pair[0][len(pair[0])-2:]=="ed" and pair[0][:len(pair[0])-2]==pair[1]) or (pair[1][len(pair[1])-2]=="ed" and pair[1][:len(pair[1])-2]==pair[0]):
        misspellings[i][2]=1
    elif (pair[0][len(pair[0])-1:]=="g" and pair[0][:len(pair[0])-1]==pair[1]) or (pair[1][len(pair[1])-1]=="g" and pair[1][:len(pair[1])-1]==pair[0]):
        misspellings[i][2]=1
    elif (pair[0].replace("_","") == pair[1]) or (pair[1].replace("_","") == pair[0]):
        misspellings[i][2]=1
    else:
        misspellings[i][2]=0
    i+=1
        


pd.DataFrame(misspellings).to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Misspellings.csv")