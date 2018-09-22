"""Analyse data from database."""
# Credit: Josh Hemann
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
from app.db.models import ImageClick
from peewee import fn

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
