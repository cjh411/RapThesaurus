# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:31:51 2017

@author: christopherhedenberg
"""

from bs4 import BeautifulSoup as bs

import requests as rqst
import pandas as pd

letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0']
artists=[]
for letter in letters:
    url = "https://genius.com/artists-index/%s" %letter

    r=rqst.get(url)
    
    data=r.text
    
    soup = bs(data)
    
    for link in soup.find_all('a'):
        string = link.get('href')
        if string != None:
            linklist=string.split("/")
        if "artists" in linklist:
            artists.append(linklist[len(linklist)-1])
            

artists_clnd=[x.replace("-","") for x in artists]
artists_clnd=[x.replace(".","") for x in artists_clnd]
artists_clnd=[x.replace("'","") for x in artists_clnd]
artists_clnd=[x.upper() for x in artists_clnd]

artdf=pd.DataFrame([artists,artists_clnd])

rapartdf=pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ArtistNames.csv")
rap_artists=list(rapartdf[rapartdf.columns.values[0]])

rap_clnd = [x.replace("-","") for x in rap_artists if isinstance(x,str)]
rap_clnd = [x.replace("[1]","") for x in rap_clnd]
rap_clnd = [x.replace("[2]","") for x in rap_clnd]
rap_clnd = [x.replace(" ","") for x in rap_clnd]
rap_clnd=[x.replace(".","") for x in rap_clnd]
rap_clnd=[x.replace("'","") for x in rap_clnd]
rap_clnd=[x.upper() for x in rap_clnd]

i=0
rap_output=[]
for artist in artists_clnd:
    if artist in rap_clnd:
        rap_output.append(artists[i])
    i+=1

pd.DataFrame([rap_output]).T.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/GeniusRapNames.csv")        

