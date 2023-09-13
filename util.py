import random


def weighted_shuffle(items, weights):
    order = sorted(range(len(items)), key=lambda i: random.random() ** (1.0 / weights[i]))
    return [items[i] for i in order]