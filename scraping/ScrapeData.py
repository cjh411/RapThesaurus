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
