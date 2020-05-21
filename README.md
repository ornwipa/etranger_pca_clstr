# L'étranger: dimensionality reduction and clustering

## Introduction

The novel, **l’Étranger** (1942) by Albert Camus, presents sentiments that may be difficult to explain. The story was earlier analysed through [visualisation](https://github.com/ornwipa/etranger_word_cloud) to present dominant sentiments and [supvervised classification](https://github.com/ornwipa/etranger_pca_clstr) to distiguish the parts where general sentiments within groups of text was rather indifferent or had intense feelings.

This program is an attempt to cluster the text in more than two groups, using **unsupervised learning**, as there can be several parts showing different type of sentiments which the previous classification to part 1 or part 2 cannot capture.

## Methods

Preprocessed [corpus](https://github.com/ornwipa/etranger_pca_clstr/blob/master/corpus.csv) was extracted from the previous analysis. In addition, to ensure there will be enough text for ngram extraction, every three paragraphs in the corpus were grouped into one. Then ngram was used as mean of feature extraction.

### Dimensionality Reduction for Feature Selection

Since there were several correlated features, a truncated singular value decomposition was used for selecting the most important features (30 out of 95) that cover the majority of the variance (80%).

![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_1.png)

### Agglomerative Clustering

As data did not meet the assumption for k-means clustering (i.e. spherical shape as shown in the below figures), hierarchical clustering was used to group the text based on their similarity. In this analysis, agglomerative clustering was used to merge the pairs of clusters that minimally decrease the linkage distance (variance in this case).

## Results

The cluster labels corresponding to each text were saved in this [table](https://github.com/ornwipa/etranger_pca_clstr/blob/master/unsup_clstr.csv).

The text may be grouped upto 4 clusters, representing different "themes". The below figures show different clusters with different colors. Only the three most important features were plots. The choice of the number of clusters could be either 2, 3, or 4.

One cluster with three primary features very close to one another (yellow, purple, red for the 2, 3, 4 clusters, respectively) include the paragraphs that constantly appear through out the book. However, the points or clusters that spreaded out more, i.e. higher variability within their own clusters, were mostly from part 2 of the book.

![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_4.png) ![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_5.png)

![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_6.png) ![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_7.png)

![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_8.png) ![alt text](https://github.com/ornwipa/etranger_pca_clstr/blob/master/results/Figure_9.png)

