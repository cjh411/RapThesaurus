import csv
import pandas as pd
import nltk
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    print(directory)
    if os.path.exists(directory):
        return 1
    else:
        return 0

path = "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/"
GenArtDf = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/GeniusArtists.csv")
ArtLists = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ArtistNames.csv")
GenRapList = pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/GeniusRapNames.csv")

missings=[]
missgenius = []
currengenius = []
geniusrap=GenRapList[GenRapList.columns.values[1]].values.tolist()
geniuslist=GenArtDf[GenArtDf.columns.values[1]].values.tolist()
artists=[x for x in ArtLists.iloc[:,0].values.tolist() if isinstance(x,str)]
artlist= [x.replace(".","").replace(",","").replace("-","").replace("'","").replace(" ","").replace("$","").replace("[1]","").replace("[2]","").upper() for x in artists]

for item in artlist:
    if item in geniuslist:
        if ensure_dir(path + GenArtDf[GenArtDf['1']==item]['0'].values[0]+"/") ==1:
            currengenius.append(item)
        else:
            missgenius.append(item)
    else:
        missings.append(item)

artistsv2=[]    
realnames={}
for item in missgenius:
    if item in geniuslist:
        artistsv2.append(GenArtDf[GenArtDf['1']==item]['0'].values[0])
        realnames[GenArtDf[GenArtDf['1']==item]['0'].values[0]] = item
        
word_dist={}
for word in missings:
    match = sorted([(refword, nltk.distance.edit_distance(refword,word)) for refword in geniuslist],key=lambda tup: tup[1],reverse=False)[0][0]
    print("%s = %s" %(word, match)) 
    word_dist[word]= match
    realnames[GenArtDf[GenArtDf['1']==match]['0'].values[0]] = word
    
artistsv2 = artistsv2 + [GenArtDf[GenArtDf['1']==word_dist.values()[i]]['0'].values[0] for i in range(len(word_dist))]
pd.DataFrame([[realnames[artist] for artist in artistsv2],artistsv2]).T.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/GeniusRapNamesv2.csv")                
