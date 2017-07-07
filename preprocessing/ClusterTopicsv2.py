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


model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecFinalModel.bin")


vocab = model.wv.vocab.keys()
vocab = [item for item in vocab if model.wv.vocab[item].count>50]
  
topicds = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicLabels.csv")
topicds.columns=['Ind','Word','Frequency','Topic']
topics = list(set(topicds['Topic'].tolist()))
topics.remove("stop")
topics.remove("other")
means = []
for item in topics:
    list2=topicds[topicds['Topic']==item]['Word'].tolist()
    means.append(sum(model[list2])/len(model[list2]))
  
topic_dists=[]  
i=0
for item in topics:
    tmp=[]
    list2=topicds[topicds['Topic']==item]['Word'].tolist()
    for word in list2:
        tmp.append(np.dot(means[i],model[word]))
    topic_dists.append(np.percentile(tmp,25))
    i+=1

topic_output=[]
for word in vocab:
    dists=[np.dot(means[i],model[word]) for i in range(len(topics))]
    index=dists.index(max(dists))
    if max(dists) > topic_dists[index]:
        topic_output.append(topics[index])
    else:
        topic_output.append("Other")
    


topic_cnt = defaultdict(int)
for item in topic_output:
    topic_cnt[item] +=1

pd.DataFrame([vocab,topic_output]).T.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/TopicsClusteredDot.csv")
            