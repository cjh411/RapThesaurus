# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:11:18 2017

@author: christopherhedenberg
"""

from bs4 import BeautifulSoup as bs

import requests as rqst
import pandas as pd
import os
import csv
import statistics

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

path = "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/"
artists=["Aesop-rock"]
artdf=pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/FinalRapNamesForGenius.csv")
artists = artdf['0'].values.tolist()
master_list=[]
for artist in artists:
    url = "https://genius.com/artists/%s" %artist

    r=rqst.get(url)
    
    data=r.text
    
    soup = bs(data)
    album_page=0
    for link in soup.find_all('a'):
        string=link.get('href')
        if "/artists/albums?for_artist_page" in string:
            album_page=1
            album_string = string
    
    if album_page==1:
        a=rqst.get("https://genius.com"+album_string).text
        soup_a=bs(a)
        for link in soup_a.find_all('a'):
            string2=link.get('href')
            if string2 != None:
                if "/albums/%s/" %artist in string2:
                    s=rqst.get("https://genius.com"+string2).text
                    soup_s=bs(s)
                    date_arr = soup_s.find('div',{"class":"metadata_unit"})
                    if date_arr != None:
                        date = date_arr.get_text()
                    for link in soup_s.find_all('a'):
                        string3 = link.get('href')
                        if string3 != None:
                            if "https://genius.com/%s" %artist in string3 and "album-art" not in string3 and "tracklist" not in string3:
                                master_list.append([artist,date,string3.split("https://genius.com/")[1]])
                            
    else:
        for link in soup.find_all('a'):
            string2=link.get('href')
            if string2 != None:
                if "/albums/%s/" %artist in string2:
                    s=rqst.get(string2).text
                    soup_s=bs(s)
                    date_arr = soup_s.find('div',{"class":"metadata_unit"})
                    if date_arr != None:
                        date = date_arr.get_text()
                    for link in soup_s.find_all('a'):
                        string3 = link.get('href')
                        if string3 != None:
                            if "https://genius.com/%s" %artist in string3 and "album-art" not in string3 and "tracklist" not in string3:
                                master_list.append([artist,date,string3.split("https://genius.com/")[1]])                               
  
master_list_copy = master_list                              
i=0
for item in master_list_copy:
    tmp = item[1].split(" ")    
    if len(tmp)>1:
        lent=len(tmp)
        master_list_copy[i][1] = tmp[lent-1]
    i+=1
           
  
master_df =pd.DataFrame(master_list_copy,columns = ["Artist","Year","Song"])
master_df.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/AlbumSongReleaseTable.csv")

artists_years=[]
for artist in artists:
    tmpdf = master_df[master_df['Artist']==artist]
    if len(tmpdf)>0:
        artists_years.append([artist,tmpdf['Year'].median(),int(tmpdf['Year'].max()),int(tmpdf['Year'].min())])
    
years = pd.DataFrame(artists_years,columns = ["Artist","Median","Max","Min"])
years.to_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ArtistYearData.csv")