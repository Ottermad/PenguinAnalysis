"""Analyse data from database."""
import numpy as np
import matplotlib.pyplot as plt
from app.db.models import ImageClick, RowAccuracy
from sklearn.cluster import MeanShift, DBSCAN


def main_analysis(run_id):
    """Main Analysis."""
    data = [
        {
            "image_path": "SPIGa/SPIGa2014b_000163.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014b_000163.JPG",
            "penguin_number": 47
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000127.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000127.JPG",
            "penguin_number": 42
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000157.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000157.JPG",
            "penguin_number": 37
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000211.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000211.JPG",
            "penguin_number": 37
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000181.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000181.JPG",
            "penguin_number": 34
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000242.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000242.JPG",
            "penguin_number": 31
        },
        {
            "image_path": "SPIGa/SPIGa2014b_000007.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014b_000007.JPG",
            "penguin_number": 43
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000015.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000015.JPG",
            "penguin_number": 36
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000025.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000025.JPG",
            "penguin_number": 35
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000039.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000039.JPG",
            "penguin_number": 33
        },
        {
            "image_path": "SPIGa/SPIGa2014a_000111.JPG",
            "file_path": "Raw_images_SPIG/SPIGa2014/SPIGa2014a_000111.JPG",
            "penguin_number": 37
        },
    ]

    # Find a value from b based upon an image.
    _, bandwidth = find_value_for_b(
        data[0]["penguin_number"],
        data[0]["image_path"]
    )

    _, eps = find_value_for_eps(
        data[0]["penguin_number"],
        data[0]["image_path"]
    )

    # Select other images and generate output
    for image in data:
        generate_row_accuracy(bandwidth, run_id, image, eps)

    # Compare images with expected number of clusters.
    rows = RowAccuracy.select().where(
        (RowAccuracy.run_id == run_id) & (RowAccuracy.algorithm == "MeanShift")
    )
    percentage_error = sum([
        (row.number_of_clusters - row.expected_number_of_clusters) /
        row.expected_number_of_clusters for row in rows
    ]) / len(rows)

    print("{}% percentage error".format(percentage_error * 100))

    rows = RowAccuracy.select().where(
        (RowAccuracy.run_id == run_id) & (RowAccuracy.algorithm == "DBSCAN")
    )
    percentage_error = sum([
        (row.number_of_clusters - row.expected_number_of_clusters) /
        row.expected_number_of_clusters for row in rows
    ]) / len(rows)

    print("{}% percentage error".format(percentage_error * 100))


def generate_row_accuracy(bandwidth, run_id, image, eps):
    """Assess how accurate an image is."""
    coords = get_coords_tuple(image["image_path"])
    image["number_of_clusters"] = find_number_of_clusters(
        bandwidth, coords)
    image["number_of_dbscan_clusters"] = find_number_of_clusters_dbscan(
        eps, coords)
    ra = RowAccuracy(
        run_id=run_id,
        algorithm="MeanShift",
        image=image["image_path"],
        number_of_clusters=image["number_of_clusters"],
        expected_number_of_clusters=image["penguin_number"]
    )
    ra.save()
    ra2 = RowAccuracy(
        run_id=run_id,
        algorithm="DBSCAN",
        image=image["image_path"],
        number_of_clusters=image["number_of_dbscan_clusters"],
        expected_number_of_clusters=image["penguin_number"]
    )
    ra2.save()


def find_number_of_clusters(bandwidth, coords):
    """Get number of clusters."""
    clustering = MeanShift(bandwidth=bandwidth).fit(coords)
    centres = clustering.cluster_centers_
    return len(centres)


def find_number_of_clusters_dbscan(eps, coords):
    """Use DBSCAN to form clusters."""
    clustering = DBSCAN(eps=eps, min_samples=2).fit(coords)
    labels = clustering.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    return n_clusters


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


def get_coords_tuple(path):
    """Get co ordinates of clicks on an image as a tuple."""
    query = ImageClick.select().where(
        (ImageClick.path == path) &
        (ImageClick.x != "NULL") &
        (ImageClick.y != "NULL")
    )

    results_x = np.array([r.x for r in query]).astype(np.float)
    results_y = [-y for y in np.array([r.y for r in query]).astype(np.float)]

    coords = np.array([(r[0], r[1]) for r in zip(results_x, results_y)])
    return coords


def plot_meanshift_clicks_on_image(path, image_file_path):
    """Plot clicks onto image."""
    query = ImageClick.select().where(ImageClick.path == path)

    b = 28
    results_x = np.array([r.x for r in query]).astype(np.float)
    results_y = [-y for y in np.array([r.y for r in query]).astype(np.float)]

    coords = np.array([(r[0], r[1]) for r in zip(results_x, results_y)])
    clustering = MeanShift(bandwidth=b).fit(coords)
    centres = clustering.cluster_centers_

    img = plt.imread(image_file_path)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 1000, -800, 0])

    ax.plot(results_x, results_y, 'bo')
    ax.plot([r[0] for r in centres], [r[1] for r in centres], 'go')
    fig.savefig('test3.png', dpi=400)


def plot_dbscan_clicks_on_image(path, image_file_path):
    """Plot clicks onto image."""
    query = ImageClick.select().where(ImageClick.path == path)

    results_x = np.array([r.x for r in query]).astype(np.float)
    results_y = [-y for y in np.array([r.y for r in query]).astype(np.float)]

    coords = np.array([(r[0], r[1]) for r in zip(results_x, results_y)])
    clustering = DBSCAN(eps=3, min_samples=2).fit(coords)
    number_of_clusters = np.amax(clustering.labels_)
    clusters = [[] for x in range(0, number_of_clusters)]
    for x in range(0, len(clustering.labels_)):
        point = clustering.labels_[x]
        try:
            clusters[point].append(coords[x])
        except:
            print(point)

    centres = []
    for cluster in clusters:
        x = sum([r[0] for r in cluster]) / len(cluster)
        y = sum([r[1] for r in cluster]) / len(cluster)
        centres.append((x, y))

    img = plt.imread(image_file_path)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 1000, -800, 0])

    ax.plot(results_x, results_y, 'bo')
    ax.plot([r[0] for r in centres], [r[1] for r in centres], 'go')
    fig.savefig('test13.png', dpi=400)


def eps_against_num_of_clusters(path):
    """Output eps values and the number of clusters for a given image."""
    coords = get_coords_tuple(path)

    for eps in range(1, 50, 5):
        number_of_clusters = find_number_of_clusters_dbscan(eps, coords)
        print("EPS: {} CLUSTERS: {}".format(eps, number_of_clusters))


def find_within_interval_eps(
    desired_number_of_clusters,
    interval,
    starting_eps,
    coords
):
    """Find value of b to get within a interval - start eps about 5."""
    eps = starting_eps
    number_of_clusters = find_number_of_clusters_dbscan(eps, coords)

    prev_op_increased = None

    while True:
        if number_of_clusters > desired_number_of_clusters + interval:
            if prev_op_increased is not None and prev_op_increased is False:
                break
            prev_op_increased = True
            eps += interval
        elif number_of_clusters < desired_number_of_clusters - interval:
            if prev_op_increased is not None and prev_op_increased is True:
                break
            prev_op_increased = False
            eps -= interval
            if eps <= 0:
                eps += interval
                break
        else:
            break
        number_of_clusters = find_number_of_clusters_dbscan(eps, coords)
    return eps, number_of_clusters


def find_value_for_eps(cluster_num, path):
    """Find a value of bandwidth for an image given number of penguins."""
    coords = get_coords_tuple(path)

    eps, number_of_clusters = find_within_interval_eps(
        cluster_num, 5, 5, coords)
    eps, number_of_clusters = find_within_interval_eps(
        cluster_num, 1, eps, coords)
    # TODO: Confirm and fix behaviour when interval = 0

    return number_of_clusters, eps
