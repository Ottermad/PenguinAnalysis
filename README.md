# Penguin Watch Data Analysis

# Data Source
Based upon Jones, F. M. et al. Time-lapse imagery and volunteer classifications from the Zooniverse Penguin Watch project. Sci. Data 5:180124 doi: 10.1038/sdata.2018.124 (2018). and data from Jones FM, Allen C, Arteta C, Arthur J, Black C, Emmerson LM, Freeman R, Hines G, Lintott CJ, Macháĉková Z, Miller G, Simpson R, Southwell C, Torsey HR, Zisserman A, Hart T (2018) Data from: Time-lapse imagery and volunteer classifications from the Zooniverse Penguin Watch project. Dryad Digital Repository. https://doi.org/10.5061/dryad.vv36g

## Aim
I have explored the use of clustering algorithms upon the data set in order to assess the accuracy and speed of the algorithms.

## Comparison of DBSCAN vs MeanShift
Thus far I have explored the DBSCAN and mean shift clustering algorithms and the comparison can be shown below.

### Speed
To execute the speed comparison run `speed_comparison.py`. Having run this locally, this produced the following results:
```
DBSCAN: Took 0.022511959075927734s
MeanShift: Took 2.7585489749908447s
```

This shows the DBSCAN algorithms to be orders of magnitude faster over the current sample (which is currently rather small).

The caveat is that MeanShift produces a cluster centre which can be plotted on an image or used for other comparison (i.e. distance between penguins). DBSCAN only produces a set of points that are part of a cluster. Therefore the below comparison also adds in the overhead of finding the mean position of all the clusters in DBSCAN.
```
DBSCAN: Took 0.018379926681518555s
DBSCAN + Cluster Centres: Took 0.02224898338317871s
MeanShift: Took 3.0717010498046875s
```

This shows even when the cluster centres have to found outside of the cluster algorithm DBSCAN is still significantly faster.

### Accuracy - Number of Penguins