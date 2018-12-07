"""Analyse data from database."""
import numpy as np
import matplotlib.pyplot as plt
from app.db.models import ImageClick, RowAccuracy
from sklearn.cluster import MeanShift
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def main_analysis():
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
    # number_of_clusters, bandwidth = find_value_for_b(
    #     data[0]["penguin_number"],
    #     data[0]["image_path"]
    # )

    # Select other images and generate output
    process_image = partial(generate_row_accuracy, 28)

    d = iter(data)

    with ProcessPoolExecutor() as executor:
        executor.map(process_image, d)

    # Compare images with expected number of clusters.


def generate_row_accuracy(bandwidth, image):
    coords = get_coords_tuple(image["image_path"])
    image["number_of_clusters"] = find_number_of_clusters(
        bandwidth, coords)
    ra = RowAccuracy(
        algorithm="MeanShift",
        image=image["image_path"],
        number_of_clusters=image["number_of_clusters"],
        expected_number_of_clusters=image["penguin_number"]
    )
    ra.save()


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


def plot_clicks_on_image(path, image_file_path):
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
