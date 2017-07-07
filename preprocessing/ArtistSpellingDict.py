# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:52:55 2017

@author: christopherhedenberg
"""

import pandas as pd
from collections import defaultdict
import pickle

ArtDict = {}
ArtClean = []
artdf=pd.read_csv('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/FinalRapNamesForGenius.csv')

artlist = artdf['0'].tolist()

for item in artlist:
    ArtDict[item.replace("-","").upper()]=item
    tmp=item.replace("-"," ").split()
    tmp =[item.capitalize() for item in tmp]
    ArtClean.append(' '.join(tmp))


pd.DataFrame({"Lookup":artlist,"Name":ArtClean}).to_csv('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtNameClean.csv') 
pickle.dump(ArtDict,open('/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ModelOutput/ArtistLookupDict.p','w'))
