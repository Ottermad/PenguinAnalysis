"""Analyse data from database."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
from app.db.models import ImageClick
from peewee import fn
from sklearn.cluster import MeanShift

def plot_bar():
    n_groups = 5

    means_men = (20, 35, 30, 35, 27)

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4

    rects1 = ax.bar(index, means_men, bar_width,
                    alpha=opacity, color='b',
                    label='Men')

    ax.set_xlabel('Group')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
    ax.legend()

    fig.tight_layout()
    plt.show()


def plot_number_of_clicks_per_image():
    query = ImageClick.select(ImageClick.path, fn.COUNT(ImageClick.id)).group_by(ImageClick.path).limit(10)
    results = query.tuples()

    n_groups = len(results)

    means_men = [r[1] for r in results]

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4

    rects1 = ax.bar(index, means_men, bar_width,
                    alpha=opacity, color='b',
                    label='Men')

    ax.set_xlabel('Group')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([r[0] for r in results])
    ax.legend()

    fig.tight_layout()
    plt.show()


def scatter_test():
    plt.plot([1, 2, 3], [1, 2, 3], 'bo')
    plt.show()


def plot_clicks_on_image(path="SPIGa/SPIGa2014b_000163.JPG"):
    query = ImageClick.select().where(ImageClick.path == path)

    results_x = np.array([r.x for r in query]).astype(np.float)
    results_y = np.array([r.y for r in query]).astype(np.float)

    coords = np.array([(r.x, r.y) for r in query]).astype(np.float)
    clustering = MeanShift(bandwidth=30).fit(coords)
    centres = clustering.cluster_centers_
    plt.plot(results_x, results_y, 'bo')
    plt.plot([r[0] for r in centres], [r[1] for r in centres], 'go')
    plt.show()
