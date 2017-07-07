# -*- coding: utf-8 -*-
"""
Created on Sun May 14 18:28:56 2017

@author: christopherhedenberg
"""

import requests as rqst
import pandas as pd
import os
import csv
import re
import math

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

path = "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/"

years = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/AlbumSongReleaseTable.csv")
#artists=["Aesop-rock"]

replace_space = [".",",","!","?",";",":","$","&","@","*","%","-"]
replace_nospace = ["'",'"']
master_lyrics=[]
master_artist = []
master_year=[]
for subdir, dirs, files in os.walk(path):
    artist = subdir.split("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/")[1]
    for filename in os.listdir(subdir):
        if ".csv" in filename and filename != 'MasterDataset.csv' and filename != 'MasterDatasetYear.csv':
            ds = pd.read_csv(subdir+"/"+filename,)
            song = filename.split(".csv")[0]
            yeararr  = years[(years['Artist']==artist) & (years['Song']==song)]['Year'].values
            if len(yeararr)>0:
                year = yeararr[0]
            else:
                year=1900
            print(subdir+"/"+filename)
            lyrics = [re.sub(r'\[[^\(]*?\]', r'', item) for item in ds[ds.columns.values[1]].values.tolist() if not isinstance(item,float) ]
            lyrics = [re.sub(r'\([^\(]*?\)', r'', item) for item in lyrics]
            lyrics = [re.sub(r'\[[^\(]*?\]', r'', item) for item in lyrics]
            for char in replace_space:
                lyrics = [x.replace(char," ") for x in lyrics]
            for char in replace_nospace:
                lyrics = [x.replace(char,"") for x in lyrics]
            lyrics = [x for x in lyrics if len(x)>20]
            lyrics = [ x[:5].strip(".") + x[5:] for x in lyrics]            
            master_lyrics =  master_lyrics + lyrics
            master_artist = master_artist + [artist for x in lyrics]
            master_year = master_year  + [year for x in lyrics]

masterds = pd.DataFrame({'artist':master_artist,'year':master_year,'lyrics':master_lyrics})  

masterds.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/MasterDatasetYear.csv")
print(masterds)  
    