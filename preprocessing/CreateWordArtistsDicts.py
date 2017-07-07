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


    
mdlds = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/MasterDatasetYear.csv")

lyrics = mdlds['lyrics'].tolist()

spellcheck = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/MisspellingsCleaned/Sheet 3-Table 1.csv")
lookup = spellcheck['Word'].tolist()
correct = spellcheck["Correct"].tolist()

spelling_dict={}
i=0
for word in lookup:
    spelling_dict[word] = correct[i]
    i+=1

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
        
#dictionary = corpora.Dictionary(texts)
#
#dictionary.save("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/RapDictionary.dict")
#
#corpus = [dictionary.doc2bow(text) for text in texts]
#
#corpora.MmCorpus.serialize('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/RapDictionary.mm', corpus)

phrases = gensim.models.phrases.Phrases(texts_clnd,min_count=25)
bigram = gensim.models.phrases.Phraser(phrases)
bigram.save('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/phraser.bin')
bigram_text = [bigram[item] for item in texts_clnd]

def spellcheck(x):
    if x in lookup:
        return spelling_dict[x]
    else:
        return x

freq_lookup ={}
for text in bigram_text:
    for token in text:
        freq_lookup[token] = token

for i in range(len(lookup)):
    freq_lookup[lookup[i]]=correct[i]
    
print("Start lookup")
bigram_text = [[freq_lookup[item] for item in verse] for verse in bigram_text]

print("End lookup")
frequency_bi = defaultdict(float)
for text in bigram_text:
    for token in text:
        frequency_bi[token] += 1
        
verse_year_dict=defaultdict(float)
for item in year_clnd:
    verse_year_dict[item]+=1
    
verse_art_dict=defaultdict(float)
for item in artists_clnd:
    verse_art_dict[item]+=1  
    
    

word_count = [[unicode(tup[0]),tup[1]] for tup in frequency_bi.items()]

pd.DataFrame(word_count,columns = ["word","frequency"]).to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordFrequencyWPhrases.csv")

word_art_dict = defaultdict(lambda: defaultdict(float))
i=0
for sent in bigram_text:
    for word in sent:
        if verse_art_dict[artists_clnd[i]]>100:
            word_art_dict[word][artists_clnd[i]]+=1
    i+=1
vocab =  word_art_dict.keys()

word_dict_sorted ={}
for word in vocab:
    for artist in word_art_dict[word].keys():
        word_art_dict[word][artist] /= verse_art_dict[artist]
    ret =  min([10,len(word_art_dict[word])-1])
    word_dict_sorted[word] = sorted(word_art_dict[word].items(),key=lambda tup: tup[1],reverse=True)[:ret]

pickle.dump( word_dict_sorted, open( "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordArtPickle/WordArtDict.p", "w" ) )


years = [1980+j for j in range(38)]
word_year_dict = defaultdict(lambda: defaultdict(float))
i=0
for sent in bigram_text:
    if year_clnd[i] > 1980:
        for word in sent:
            word_year_dict[word][year_clnd[i]]+=1
    i+=1

vocab =  word_year_dict.keys()

word_year_sorted ={}
for word in vocab:
    for year in word_year_dict[word].keys():
        word_year_dict[word][year] /= verse_year_dict[year]
    word_year_sorted[word] = sorted(word_year_dict[word].items(),key=lambda tup: tup[1],reverse=True)

pickle.dump( word_year_sorted, open( "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordTimePickle/WordYearDict.p", "w" ) )



art_word_dict = defaultdict(lambda: defaultdict(float))
i=0
for sent in bigram_text:
    for word in sent:
        art_word_dict[artists_clnd[i]][word]+=1
    i+=1
vocab =  art_word_dict.keys()

art_word_dict_sorted ={}
for word in vocab:
    for word2 in art_word_dict[word]:
        art_word_dict[word][word2] /= frequency_bi[word2]
    ret =  min([100,len(art_word_dict[word])-1])
    art_word_dict_sorted[word] = sorted(art_word_dict[word].items(),key=lambda tup: tup[1],reverse=True)[:ret]

pickle.dump( art_word_dict_sorted, open( "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtWordPickle/ArtWordDict.p", "wb" ) )



art_word_dict2 = defaultdict(lambda: defaultdict(float))
i=0
for sent in bigram_text:
    for word in sent:
        art_word_dict2[artists_clnd[i]][word]+=1
    i+=1
vocab =  art_word_dict2.keys()

art_word_dict_sorted2 ={}
for word in vocab:
    for word2 in art_word_dict2[word]:
        art_word_dict2[word][word2] /= frequency_bi[word2]
    ret =  min([100,len(art_word_dict2[word])-1])
    art_word_dict_sorted2[word] = sorted(art_word_dict2[word].items(),key=lambda tup: tup[1],reverse=True)[:ret]

pickle.dump( art_word_dict_sorted, open( "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtWordPickle/ArtWordDict.p", "wb" ) )

#sentences = []
#for i in range(len(texts)):
#    sentences.append(LabeledSentence(texts[i],[artists[i]]))
#
#
#size=50   
#model = gensim.models.Doc2Vec(sentences,min_count=10,size=size,workers=4,window=8,dbow_words=1)
#
#
#artists = model.docvecs.offset2doctag
#
#master=[]
#columns = ["dim_%s" for i in range(1,size+1)] +["artist"]
#for artist in artists:
#    master.append(list(model.docvecs.doctag_syn0[model.docvecs.offset2doctag.index(artist)]) + [artist])
#    
#pd.DataFrame(master,columns=columns).to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtistVectors.csv")
#
#
#model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecRapModel.bin")
#
#
#X = np.concatenate([model[model.wv.vocab],model.docvecs.doctag_syn0norm])
#
#X=model.docvecs.doctag_syn0norm
