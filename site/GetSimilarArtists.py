# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 14:14:00 2017

@author: christopherhedenberg
"""


import numpy as np
from numpy import exp, log, dot, zeros, outer, random, dtype, float32 as REAL,\
    double, uint32, seterr, array, uint8, vstack, fromstring, sqrt, newaxis,\
    ndarray, empty, sum as np_sum, prod, ones, ascontiguousarray
from gensim import matutils
import pandas as pd

def GetSimilarArtistsWord(model,positive,negative=[],topn=10):

    
    pos_dists = [((1 + np.dot(model.docvecs.doctag_syn0, model[term])) / 2) for term in positive]
    neg_dists = [((1 + np.dot(model.docvecs.doctag_syn0, model[term])) / 2) for term in negative]
    if len(negative)==0:
        dists = np.prod(pos_dists, axis=0) 
    else:
        dists = np.prod(pos_dists, axis=0) / (np.prod(neg_dists, axis=0) + 0.000001)
    
    best = matutils.argsort(dists, topn=topn, reverse=True)
    # ignore (don't return) words from the input
    result = [(model.docvecs.offset2doctag[sim], float(dists[sim])) for sim in best]
    return result[:topn]
   
def GetSimilarArtists(model,artarr, positive,negative=[],topn=10):

    
    pos_dists = [((1 + np.dot(artarr, artarr[model.docvecs.offset2doctag.index(term)])) / 2) for term in positive]
    neg_dists = [((1 + np.dot(artarr, artarr[model.docvecs.offset2doctag.index(term)])) / 2) for term in negative]
    if len(negative)==0:
        dists = np.prod(pos_dists, axis=0) 
    else:
        dists = np.prod(pos_dists, axis=0) / (np.prod(neg_dists, axis=0) + 0.000001)
    
    best = matutils.argsort(dists, topn=topn, reverse=True)
    # ignore (don't return) words from the input
    result = [(model.docvecs.offset2doctag[sim], float(dists[sim])) for sim in best]
    return result[:topn]

def GetSimilarArtistsRap(model,artarr, input_vec,topn=10):

    input_vec_norm = (input_vec / sqrt((input_vec** 2).sum(-1))[..., newaxis]).astype(REAL)
    print(input_vec_norm)
    pos_dists = ((1 + np.dot(artarr, input_vec_norm)) / 2) 
    
    best = matutils.argsort(pos_dists, topn=topn, reverse=True)
    # ignore (don't return) words from the input
    result = [(model.docvecs.offset2doctag[sim], float(pos_dists[sim])) for sim in best]
    return result[:topn]
    
def GetSimilarWordArtists(model,positive,negative=[],topn=10):

    
    pos_dists = [((1 + np.dot(model[model.wv.vocab], model.docvecs.doctag_syn0[model.docvecs.offset2doctag.index(term)])) / 2) for term in positive]
    neg_dists = [((1 + np.dot(model[model.wv.vocab], model.docvecs.doctag_syn0[model.docvecs.offset2doctag.index(term)])) / 2) for term in negative]
    if len(negative)==0:
        dists = np.prod(pos_dists, axis=0) 
    else:
        dists = np.prod(pos_dists, axis=0) / (np.prod(neg_dists, axis=0) + 0.000001)
    
    best = matutils.argsort(dists, topn=topn, reverse=True)
    # ignore (don't return) words from the input
    result = [(model.wv.index2word[sim], float(dists[sim])) for sim in best]
    return result[:topn]