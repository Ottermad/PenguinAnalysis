"""Analyse data from database."""
import time
import uuid
from functools import partial
from app.db.models import RowAccuracy
from .meanshift import find_number_of_clusters, find_value_for_b
from .helper import get_coords_tuple
from .dbscan import find_number_of_clusters_dbscan, find_value_for_eps

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


def accuracy_comparison():
    """Main Analysis."""
    run_id = uuid.uuid4()

    # Find a value for b based upon an image.
    _, bandwidth = find_value_for_b(
        data[0]["penguin_number"],
        data[0]["image_path"]
    )

    # Find a value for eps based upon an image.
    _, eps = find_value_for_eps(
        data[0]["penguin_number"],
        data[0]["image_path"]
    )

    number_of_dbscan_clusters = partial(find_number_of_clusters_dbscan, eps)
    number_of_meanshift_clusters = partial(find_number_of_clusters, bandwidth)

    # Select other images and generate output
    for image in data:
        generate_row_accuracy(
            number_of_dbscan_clusters, run_id, image, "DBSCAN")
        generate_row_accuracy(
            number_of_meanshift_clusters, run_id, image, "MeanShift")

    # Compare images with expected number of clusters.

    for a in ["DBSCAN", "MeanShift"]:
        rows = RowAccuracy.select().where(
            (RowAccuracy.run_id == run_id) & (RowAccuracy.algorithm == a)
        )
        percentage_error = sum([
            (row.number_of_clusters - row.expected_number_of_clusters) /
            row.expected_number_of_clusters for row in rows
        ]) / len(rows)

        print("{}: {}% percentage error".format(a, percentage_error * 100))


def generate_row_accuracy(number_of_clusters_func, run_id, image, algorithm):
    """Assess how accurate an image is."""
    coords = get_coords_tuple(image["image_path"])
    number_of_clusters = number_of_clusters_func(coords)
    ra = RowAccuracy(
        run_id=run_id,
        algorithm=algorithm,
        image=image["image_path"],
        number_of_clusters=number_of_clusters,
        expected_number_of_clusters=image["penguin_number"]
    )
    ra.save()


def speed_comparison():
    """Compare the speed of clustering algorithms."""
    coords = [get_coords_tuple(image["image_path"]) for image in data]

    algorithms = [
        {
            "name": "DBSCAN",
            "func": partial(find_number_of_clusters_dbscan, 20)
        },
        {
            "name": "MeanShift",
            "func": partial(find_number_of_clusters, 30)
        }
    ]

    for a in algorithms:
        start = time.time()
        for coord in coords:
            a["func"](coord)
        end = time.time()
        print("{}: Took {}s".format(a["name"], end - start))
