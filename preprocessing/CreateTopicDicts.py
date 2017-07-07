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
from gensim import utils, matutils 
import pickle

model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecFinalModel.bin")


vocab = model.wv.vocab.keys()
vocab = [item for item in vocab if model.wv.vocab[item].count>50]
  
topicds = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicsClusteredDotv1.csv")
topicds.columns=['Ind','Word','Topic']
topics = list(set(topicds['Topic'].tolist()))
topics.remove("Other")
  
topic_topword=[]  
for item in topics:
    list2=topicds[topicds['Topic']==item]['Word'].tolist()
    list2cnt = [model.wv.vocab[word].count for word in list2]
    topic_topword.append(list2[list2cnt.index(max(list2cnt))])

    
topic_cnt = defaultdict(int)
for item in topics:
    list2=topicds[topicds['Topic']==item]['Word'].tolist()
    for item2 in list2:
        topic_cnt[item] +=model.wv.vocab[item2].count
topic_cntlist=[]
for item in topics:
    topic_cntlist.append(topic_cnt[item])

pd.DataFrame([topics,topic_cntlist,topic_topword]).T.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicCountTotal.csv")
            