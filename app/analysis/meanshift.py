"""Functions related to MeanShift."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift
from app.db.models import ImageClick
from .helper import get_coords_tuple


def find_number_of_clusters(bandwidth, coords):
    """Get number of clusters."""
    clustering = MeanShift(bandwidth=bandwidth).fit(coords)
    centres = clustering.cluster_centers_
    return len(centres)


def find_within_interval(
    desired_number_of_clusters,
    interval,
    starting_bandwith,
    coords
):
    """Find value of b to get within a interval."""
    bandwidth = starting_bandwith
    number_of_clusters = find_number_of_clusters(bandwidth, coords)

    prev_op_increased = None

    while True:
        if number_of_clusters > desired_number_of_clusters + interval:
            if prev_op_increased is not None and prev_op_increased is False:
                break
            prev_op_increased = True
            bandwidth += interval
        elif number_of_clusters < desired_number_of_clusters - interval:
            if prev_op_increased is not None and prev_op_increased is True:
                break
            prev_op_increased = False
            bandwidth -= interval
        else:
            break
        number_of_clusters = find_number_of_clusters(bandwidth, coords)
    return bandwidth, number_of_clusters


def find_value_for_b(cluster_num, path):
    """Find a value of bandwidth for an image given number of penguins."""
    coords = get_coords_tuple(path)

    b, number_of_clusters = find_within_interval(47, 5, 1, coords)
    b, number_of_clusters = find_within_interval(47, 1, b, coords)
    # TODO: Confirm and fix behaviour when interval = 0

    return number_of_clusters, b


def plot_meanshift_clicks_on_image(path, image_file_path, bandwidth):
    """Plot clicks onto image."""
    coords = get_coords_tuple(path)
    clustering = MeanShift(bandwidth=bandwidth).fit(coords)
    centres = clustering.cluster_centers_

    img = plt.imread(image_file_path)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 1000, -800, 0])

    ax.plot([c[0] for c in coords], [c[1] for c in coords], 'bo')
    ax.plot([r[0] for r in centres], [r[1] for r in centres], 'go')
    fig.savefig('test3.png', dpi=400)
