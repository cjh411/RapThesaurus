# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 08:52:48 2017

@author: n0267335
"""

from flask import Flask, flash, redirect, render_template, request, session, url_for
import pandas as pd
from tempfile import gettempdir
from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure,ColumnDataSource, show
import numpy as np
import sys
sys.path.insert(0, "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/templates2")
import CreateArtistGraph
import CreateWordGraph
import CreateWordYearGraph
import CreateWordArtGraphRect
import CreateTopicGraph
import GetSimilarArtists
import CreateArtWordGraphRect
import gensim
from random import randint
import pickle
from numpy import exp, log, dot, zeros, outer, random, dtype, float32 as REAL,\
    double, uint32, seterr, array, uint8, vstack, fromstring, sqrt, newaxis,\
    ndarray, empty, sum as np_sum, prod, ones, ascontiguousarray
replace_space = [".",",","!","?",";",":","$","&","@","*","%"]
replace_nospace = ["'",'"']

# configure application
app = Flask(__name__, template_folder="/Users/christopherhedenberg/Downloads/projects/RapThesaurus/templates2/templates",
            static_folder = "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/templates2/static")
#app = Flask(__name__)

model =gensim.models.Doc2Vec.load("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/Doc2VecFinalModel.tx")

wordArtYear=pickle.load(open("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordTimePickle/WordYearDict.p",'rb'))

wordArt=pickle.load(open("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/WordArtPickle/WordArtDict.p",'rb'))
normArt= (model.docvecs.doctag_syn0 / sqrt((model.docvecs.doctag_syn0 ** 2).sum(-1))[..., newaxis]).astype(REAL)
artWord=pickle.load(open("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtWordPickle/ArtWordDict.p",'rb'))
artWordCnt=pickle.load(open("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtWordPickle/ArtWordDictCnt.p",'rb'))
artLookup = pickle.load(open('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtistLookupDict.p','rb'))
artLookupClean = pickle.load(open('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtistLookupCleanDict.p','rb'))
artKeys = artLookup.keys()
spellcheck = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/MisspellingsCleaned/Sheet 3-Table 1.csv")
lookup = spellcheck['Word'].tolist()
correct = spellcheck["Correct"].tolist()

spelling_dict={}
i=0
for word in lookup:
    spelling_dict[word] = correct[i]
    i+=1
vocab = model.wv.vocab.keys()
vocab = [item for item in vocab if model.wv.vocab[item].count>500]
vocab_full = model.wv.vocab.keys()
artist_list = model.docvecs.offset2doctag
phraser  = gensim.models.phrases.Phraser.load('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/phraser.bin')
@app.errorhandler(404)
def route404(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def route500(e):
    return render_template("404.html"), 500
    
@app.route("/",methods=["GET"])
def filters(): 
        script1,div1 = CreateArtistGraph.createArtGraph()
        script2,div2 = CreateTopicGraph.createTopicGraph()   
        script3,div3 = CreateWordGraph.createWordGraph()
        return render_template("HomePage.html",script1=script1,div1=div1, script2=script2,div2=div2,script3=script3,div3=div3)
        
@app.route("/words",methods=["GET","POST"])
def words(): 
    if request.method == 'POST':
        randwrd = str(request.form.get("wordInput"))
        randwrd_cln = randwrd
        bigram_neg=[]
        randarr=[]
        for char in replace_space:
            randwrd_cln = randwrd_cln.replace(char," ")
        for char in replace_nospace:
            randwrd_cln = randwrd_cln.replace(char,"")
        if "+" in randwrd_cln or "-" in randwrd_cln:
            randwrd_cln = randwrd_cln.replace(" ","")
            if "-" not in randwrd_cln:
                randarr=randwrd_cln.split("+")
            else: 
                rand = [item.split("-") for item in randwrd_cln.split("+")]
                for item in rand:
                    if len(item)==1:
                        randarr.append(item[0])
                    else:
                        randarr.append(item[0])
                        bigram_neg = bigram_neg+item[1:]
            bigram_neg=[item.lower() for item in bigram_neg]
            randarr=[item.lower() for item in randarr]
            for i in range(len(randarr)):
                if randarr[i] in lookup:
                    randarr[i] = spelling_dict[randarr[i]]
            for i in range(len(bigram_neg)):
                if bigram_neg[i] in lookup:
                    bigram_neg[i] = spelling_dict[bigram_neg[i]]
            bigram_arr = [item for item in randarr if item in vocab_full]
            bigram_neg = [item for item in bigram_neg if item in vocab_full]               
            if len(bigram_arr)>0 :
                synns=[tup[0].replace("_"," ") for tup in model.most_similar_cosmul(positive=bigram_arr,negative=bigram_neg)]
                return render_template("ExploreWordResultParams.html",syns = synns,rndwrd=randwrd.replace("_"," "))
            else:
                return render_template("404.html") 
        else:
            randarr = [item.lower() for item in randwrd_cln.split()]
        for i in range(len(randarr)):
            if randarr[i] in lookup:
                randarr[i] = spelling_dict[randarr[i]]
        bigram_arr = phraser[randarr]
        if len(bigram_arr)==1 and len(bigram_neg)==0:
            if bigram_arr[0] in vocab_full:
                synns=[tup[0].replace("_"," ") for tup in model.most_similar_cosmul(bigram_arr[0])]
                script,div = CreateWordYearGraph.createWordYearGraph(randwrd_cln,wordArtYear[bigram_arr[0]])
                script1,div1= CreateWordArtGraphRect.createWordArtGraph(wordArt[bigram_arr[0]])
                return render_template("ExploreWordResultParams.html",syns = synns,rndwrd=randwrd.replace("_"," "),script1=script,div1=div,script2=script1,div2=div1)
            else:
                return render_template("404.html")
        else:
            bigram_arr = [item for item in bigram_arr if item in vocab_full]
            if len(bigram_arr)>0 :
                synns=[tup[0].replace("_"," ") for tup in model.most_similar_cosmul(positive=bigram_arr)]
                script,div = CreateWordYearGraph.createWordYearGraph(randwrd_cln,wordArtYear[bigram_arr[0]])
                script1,div1= CreateWordArtGraphRect.createWordArtGraph(wordArt[bigram_arr[0]])
                return render_template("ExploreWordResultParams.html",syns = synns,rndwrd=randwrd.replace("_"," "),script1=script,div1=div,script2=script1,div2=div1)
            else:
                return render_template("404.html") 
    elif request.method == 'GET':
        randwrd=vocab[randint(0,len(vocab))]
        synns=[tup[0].replace("_"," ") for tup in model.most_similar_cosmul(randwrd)]
        script,div = CreateWordYearGraph.createWordYearGraph(randwrd,wordArtYear[randwrd])
        return render_template("ExploreWordReturnParams.html",syns = synns,rndwrd=randwrd.replace("_"," "),script1=script,div1=div)
        
 
@app.route("/artists",methods=["GET","POST"])       
def artists():
    if request.method == 'POST':
        randwrd = str(request.form.get("wordInput"))
        art_lookup=randwrd.replace("'","").replace("$","").replace("-","").replace(".","").replace(",","").replace("#","").replace(" ","").upper()
        if art_lookup in artKeys:
            art_clnd = artLookup[art_lookup]
            synns=[tup[0] for tup in GetSimilarArtists.GetSimilarArtists(model,normArt,[art_clnd])]
            script,div = CreateArtWordGraphRect.createArtWordGraph(artWord[art_clnd])
            script1,div1 = CreateArtWordGraphRect.createArtWordGraph(artWordCnt[art_clnd])
            return render_template("ExploreArtistResultParams.html",syns = synns,rndwrd=randwrd.replace("_"," "),script1=script,div1=div,script2=script1,div2=div1)
        else:
            return render_template("404.html")
    elif request.method == 'GET':
        randwrd=artist_list[randint(0,len(artist_list))]
        synns=[tup[0] for tup in GetSimilarArtists.GetSimilarArtists(model,normArt,[randwrd])]
        return render_template("ExploreArtistReturnParams.html",syns = synns,rndwrd=randwrd.replace("_"," "))
        
 
    
@app.route("/raps",methods=["GET","POST"])       
def raps():
    if request.method == 'POST':
        text= str(request.form.get("rapBox"))
        text_list= [item.replace("'","").replace(",","").replace("-"," ").lower() for item in text.split()]
        vec_rep = np.zeros(50,dtype=np.float32)
        text_list =[item for item in text_list if item in vocab_full]
        text_vec=model[text_list]
        text_vec= (text_vec / sqrt((text_vec ** 2).sum(-1))[..., newaxis]).astype(REAL)
        vec_rep=sum(text_vec)#/len(text_vec)
        synns=[tup[0] for tup in GetSimilarArtists.GetSimilarArtistsRap(model,normArt,vec_rep)]
        return render_template("RapResultParams.html",syns = synns,rndwrd='1990')
    elif request.method == 'GET':
        return render_template("RapReturn.html")
     

app.run()