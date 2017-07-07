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
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np


model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecFinalModel.bin")




artists = model.docvecs.offset2doctag
wordsdf = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/FinalTopicList.csv")
wordfreq = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordFrequencyWPhrases.csv")
wordfreq = wordfreq.sort(columns=['frequency'],ascending = False)[:1000]

Xin = [item for item in wordfreq['word'].tolist() if np.isnan()]
words = wordsdf['Word'].tolist()
X = model[wordfreq['word'].tolist()]


tsne = TSNE(n_components=2,early_exaggeration=12,perplexity=15)

X_tsne = tsne.fit_transform(X)
X_tsne_words = X_tsne[:len(model[model.wv.vocab])]
X_tsne_words_df = pd.DataFrame(X_tsne_words)
X_tsne_words_df['Word'] = model.wv.vocab.keys()
X_tsne_words_df.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordTSNEFinalModel.csv")



artistdf = pd.DataFrame(X_tsne[len(model[model.wv.vocab]):])
artistdf['Artist'] = model.docvecs.doctag_syn0

artistdf.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtistTSNEFinalModel.csv")
#plt.scatter(X_tsne[34211:, 0], X_tsne[34211:, 1])
#plt.scatter(X_tsne[:,0],X_tsne[:,1])
#plt.show()
