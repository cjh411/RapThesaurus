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



model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecFinalModel.bin")

  
topicds = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicLabels.csv")

topics = list(set(topicds[topicds['frequency']>50]['Unnamed: 3'].tolist()))

vocab =topicds[topicds['frequency']>50]['word'].tolist()

topic_output = {}
for item in vocab:
    topic_output[item] = []
    
for item in topics:
    if item != 'other' and item != 'stop':
        search_words = topicds[topicds['Unnamed: 3']==item]['word'].tolist()
        for word in search_words:
            if word in vocab:
                topic_output[word].append(item)
                grid1 = [pair for pair in model.most_similar_cosmul(word,topn=30) if pair[1]>.8 ]
            for syn1 in grid1:
                if syn1[0] in vocab:    
                    if item not in topic_output[syn1[0]]:
                        if model.similarity(syn1[0],word) > .5:
                            topic_output[syn1[0]].append(item)
                    grid2 = [pair for pair in model.most_similar_cosmul(syn1[0],topn=30) if pair[1]>.8 ]
                    for syn2 in grid2:
                        if syn2[0] in vocab:
                            if item not in topic_output[syn2[0]]:
                                if model.similarity(syn2[0],word) > .5:
                                    topic_output[syn2[0]].append(item)
              
df = pd.DataFrame.from_dict(topic_output,orient='index')     

df.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicListDups.csv")          