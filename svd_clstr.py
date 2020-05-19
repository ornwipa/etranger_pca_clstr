#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:08:42 2020

@author: ornwipa
"""

import math
import nltk
# nltk.download('stopwords')
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def combineData(data):
    ''' to reduce the effect of short paragraphs ...
    combine corpus text by shrinking each of 3 rows in to one,
    the 204 rows are reshaped to 68 rows '''
    new_data = []
    for i in range(len(data)):
        if i % 3 == 0:
            text = ''
        text += data[i]
        if i % 3 == 2:
            new_data.append(text)
    return new_data

def selectNgramFeatures(data):
    ''' text here is a list of paragraph for creating ... 
    ... sparse matrix of (n_samples, n_features) '''
    arrêt = set(nltk.corpus.stopwords.words('french')) # 'stopwords' en français
    arrêt = arrêt.union({'avoir', 'être', 'ça', 'cela', 'cet', 'cette'})
    ''' 'buid ngram model: unigram, bigram, trigram '''
    vectorizer = CountVectorizer(ngram_range = (2, 6), 
                                 min_df = 0.01, max_df = 0.8, 
                                 max_features = 300, 
                                 strip_accents = None,                                                                                
                                 # use_idf = True, smooth_idf = True, 
                                 # sublinear_tf = True, 
                                 stop_words = arrêt)
    return (vectorizer, vectorizer.fit_transform(data))    

def analyzeSVD(sparse_matrix, data):
    ''' perform singular values decomposition of the sparse matrix,
    and plot reduced dimensionalities to choose the number of features,
    serves as analysis module, do not return anything but a plot '''
    X = sparse_matrix
    svd = TruncatedSVD(n_components = len(data))    
    svd.fit_transform(X)
    var_ratio = svd.explained_variance_ratio_
    var_ratio_cum = []
    for j in range(len(var_ratio)):
        var_ratio_cum.append(sum(var_ratio[:(j+1)]))
    plt.figure()
    plt.plot(var_ratio_cum, '-', color='black')
    plt.xlabel('Number of features')
    plt.ylabel('Ratio of variance explained')    
    
def analyzeClustering(data, max_num_clusters):
    ''' perform k-means clustering with various number of clusters,
    plot predicted clusters, and their inertia by number of clusters,
    serves as analysis module, do not return anything but plots '''
    ks = range(1, max_num_clusters)
    colors = ['indigo', 'orange', 'green', 'red', 'cyan', 'blue']
    # AIC = [] # Akaike information criterion for the current model on the input X
    plt.figure()
    for k in ks:
        ''' fit model and calculate inertia '''
        model = AgglomerativeClustering(n_clusters = k)
        # model = GaussianMixture(n_components = k, init_params = 'random') 
        # model = KMeans(n_clusters = k)
        # model = SpectralClustering(n_clusters = k, assign_labels = 'kmeans',
        #                           affinity = 'nearest_neighbors')
        model.fit(data)
        # AIC.append(model.aic(data))
        ''' use model to predict clusters and plots '''
        # y_predict = model.predict(data)
        y_predict = model.labels_
        y_plot = []
        for i in y_predict:
            y_plot.append(colors[i])
        ax = Axes3D(plt.figure())
        ax.scatter(data[0], data[1], data[2], edgecolor = 'k', c = y_plot)
        ax.set_xlabel('Feature 1')
        ax.set_ylabel('Feature 2')
        ax.set_zlabel('Feature 3')
        plt.title(str(k) + ' clusters/components')
        frame = pd.DataFrame(data)
        frame['cluster'] = y_predict
        plt.figure()
        plt.subplot(233)
        for k in range(5):
            datak = frame[frame['cluster']==k]
            plt.scatter(datak[0], datak[1], c = colors[k], s = 5)
            plt.xlabel('Feature 1')
            plt.ylabel('Feature 2')
        plt.subplot(236)
        for k in range(5):
            datak = frame[frame['cluster']==k]
            plt.scatter(datak[0], datak[2], c = colors[k], s = 5)  
            plt.xlabel('Feature 1')
            plt.ylabel('Feature 3')
        plt.show()
    # plt.figure()
    # plt.bar(ks, AIC, color = 'black')
    # plt.xlabel('Number of clusters/components')
    # plt.ylabel('AIC') # the lower AIC the better

def main():
    ''' prepare data in sparse matrix '''
    data = list(pd.read_csv('corpus.csv')['texte'])
    data = combineData(data)
    vect, X = selectNgramFeatures(data)
    # print(vect.get_feature_names(), len(vect.get_feature_names()))
    ''' perform SVD of the sparse matrix, 
    plot variance explained by the number of features '''
    analyzeSVD(X, data) 
    ''' continue once select the number of components '''
    svd = TruncatedSVD(n_components = 30)
    X_new = pd.DataFrame(svd.fit_transform(X))
    print(svd.singular_values_)
    ''' perform clustering and analyze the proper number of clusters,
    with 3D and 2D visualization '''
    analyzeClustering(X_new, 6) # set max to 5 clusters    
    model = AgglomerativeClustering(n_clusters = 4) 
    label = model.fit_predict(X_new)
    print(label)
    frame = pd.DataFrame(data)
    frame.columns = ['texte']
    frame['cluster'] = label
    frame.to_csv('unsup_clstr.csv')
    

if __name__ == "__main__":
    main()
    