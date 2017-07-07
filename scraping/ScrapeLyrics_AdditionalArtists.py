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


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

path = "/Users/christopherhedenberg/Downloads/projects/RapThesaurus/data/"
artists=["Aesop-rock"]
artdf=pd.read_csv("/Users/christopherhedenberg/Downloads/projects/RapThesaurus/ArtistsManualList.csv")
artists = artdf['0'].values.tolist()
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
                    for link in soup_s.find_all('a'):
                        string3 = link.get('href')
                        if string3 != None:
                            if "https://genius.com/%s" %artist in string3 and "album-art" not in string3 and "tracklist" not in string3:
                                print(string3)                                
                                l=rqst.get(string3).text
                                soup_l=bs(l)
                                song=[]
                                lyrics = soup_l.find('div',{"class":"lyrics"})
                                if lyrics != None:
                                    text=lyrics.get_text()
                                    song2 = lyrics.get_text().encode("utf-8").replace("[Ve","|[Ve").replace("[Ho","|[Ho").replace("[Ch","|[Ch").replace("[Br","|[Br").replace("[Out","|[Out").replace("[In","|[In").split("|")
                                    song2 = [verse.replace("\n",".") for verse in song2]                                        
                                    namearr = string3.split("/")
                                    filenm="%s/%s/%s.csv"%(path,artist,namearr[len(namearr)-1])
                                    ensure_dir(filenm)
                                    print(filenm)
            #                                    text_file = open(filenm, "w")
            #                                    text_file.write(str(text))
            #                                    text_file.close()
                                    with open(filenm, 'w') as myfile:
                                        wr = csv.writer(myfile)
                                        for verse in song2:
                                            wr.writerow([artist,verse])
    else:
        for link in soup.find_all('a'):
            string2=link.get('href')
            if string2 != None:
                if "/albums/%s/" %artist in string2:
                    s=rqst.get(string2).text
                    soup_s=bs(s)
                    for link in soup_s.find_all('a'):
                        string3 = link.get('href')
                        if string3 != None:
                            if "https://genius.com/%s" %artist in string3 and "album-art" not in string3 and "tracklist" not in string3:
                                print(string3)                                
                                l=rqst.get(string3).text
                                soup_l=bs(l)
                                song=[]
                                lyrics = soup_l.find('div',{"class":"lyrics"})
                                if lyrics != None:
                                    text=lyrics.get_text()
                                    song2 = lyrics.get_text().encode("utf-8").replace("[Ve","|[Ve").replace("[Ho","|[Ho").replace("[Ch","|[Ch").replace("[Br","|[Br").replace("[Out","|[Out").replace("[In","|[In").split("|")
                                    song2 = [verse.replace("\n",".") for verse in song2]                                        
                                    namearr = string3.split("/")
                                    filenm="%s/%s/%s.csv"%(path,artist,namearr[len(namearr)-1])
                                    ensure_dir(filenm)
                                    print(filenm)
            #                                    text_file = open(filenm, "w")
            #                                    text_file.write(str(text))
            #                                    text_file.close()
                                    with open(filenm, 'w') as myfile:
                                        wr = csv.writer(myfile)
                                        for verse in song2:
                                            wr.writerow([artist,verse])        
            
                
            
