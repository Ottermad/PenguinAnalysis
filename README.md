# Penguin Watch Data Analysis

# Data Source
Based upon Jones, F. M. et al. Time-lapse imagery and volunteer classifications from the Zooniverse Penguin Watch project. Sci. Data 5:180124 doi: 10.1038/sdata.2018.124 (2018). and data from Jones FM, Allen C, Arteta C, Arthur J, Black C, Emmerson LM, Freeman R, Hines G, Lintott CJ, Macháĉková Z, Miller G, Simpson R, Southwell C, Torsey HR, Zisserman A, Hart T (2018) Data from: Time-lapse imagery and volunteer classifications from the Zooniverse Penguin Watch project. Dryad Digital Repository. https://doi.org/10.5061/dryad.vv36g

## Aim
I have explored the use of clustering algorithms upon the data set in order to assess the accuracy and speed of the algorithms.

## Comparison of DBSCAN vs MeanShift
Thus far I have explored the DBSCAN and Mean Shift clustering algorithms and the comparison can be shown below.

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
One question you could ask about an image is how many penguins are there? By applying a clustering algorithm to the user's clicks on the data you can estimate the number of penguins by looking the number of clusters. In order to compare the DBSCAN and MeanShift algorithms I manually looked at images and counted the number of penguins then I applied the two algorithms to the images and compared my count to the number of clusters generated by then. I then took the mean of the absolute differences between number of clusters and the expected number of clusters. This gave me these results:
```
DBSCAN: 2.3636363636363638 mean number of clusters away
MeanShift: 3.3636363636363638 mean number of clusters away
```

This shows that DBSCAN appears to be more accurate although the difference is vary small and may be insignificant. 

This can be done by executing `accuracy_comparison.py`

#### Determining values for EPS and Bandwidth
The DBSCAN algorithm heavily on EPS which is described by the [Scikit-Learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN) as "the maximum distance between two samples for them to be considered as in the same neighborhood".

The MeanShift clustering algorithm depends on a parameter known as bandwidth (see [here](https://spin.atomicobject.com/2015/05/26/mean-shift-clustering/) for a great layman's explanation of it).

In order to determine a value for this parameter two functions `find_value_for_b` and `find_value_for_eps` were implemented which both similar approaches. They start by taking an image with an known number of clusters/penguins, a set of clicks for that image and starting value for eps/bandwidth. They then run the clustering algorithm and then if the number of clusters is lower than the expected number then the value for eps/bandwidth is increased. This repeats until the number of clusters starts to decrease. At this point eps/bandwidth is set back to when it was increasing a smaller increment is added to it until it starts to decrease again. 

To improve this process a mean could be taken after running this process over several images. 

## Running the code locally
I am using Python 3.5 and Postgres 11

In order to run the code you will first need a Postgres database running. The default database name and port are penguin_db and 5433 (Note: this is different to the default postgres port due to local issues and will be resolved soon). These can be configured in `app/db/constants.py`

To install the necessary python packages run:
`pip install -r requirements.txt`

Then to set up the schema run:
`python create_tables.py`

To import the data create a directory named `click_data` in the same directory as `app` and in place the csv you wish to work with. The csvs can be found (https://datadryad.org/resource/doi:10.5061/dryad.vv36g)[here] under PW Anonymised Raw Classifications and Metadata (update)
Then run:
`python import_data.py`

You can then run the rest of code such as:
`python speed_comparison.py`
