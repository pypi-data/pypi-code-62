"""Module with tools for predicting events

Todo:
    * Use dense layers for multi-class prediction
"""

import math

import numpy as np


def distance_measure(array_1, array_2):
    """Finds distance between two ndarrays

    Args:
        array_1 (ndarray) -- First array of two to calculate distance
        array_2 (ndarray) -- Second array of two to calculate distance

    Returns:
        distance (float) -- Distance between array_1 and array_2
            as calculated in Eqn. 10, Sec. 3.3 of
            "Time Series Segmentation through Automatic Feature Learning"
            <https://arxiv.org/abs/1801.05394>
    """

    if not isinstance(array_1, np.ndarray):
        raise TypeError("Expected {} got {}".format(np.ndarray, type(array_1)))

    if not isinstance(array_2, np.ndarray):
        raise TypeError("Expected {} got {}".format(np.ndarray, type(array_2)))

    # Using the frobenius norm from np.linalg.norm()
    norm_array_1 = np.linalg.norm(array_1)
    norm_array_2 = np.linalg.norm(array_2)

    diff = array_1 - array_2

    norm_diff = np.linalg.norm(diff)

    distance = norm_diff / math.sqrt(norm_array_1 * norm_array_2)

    return distance


def get_events(distance_list, threshold):
    """Finds index of events based on the distances in distance list
    and threshold for detecting as event

    Args:
        distance_list (list of float) -- List of distances over
            many timeframes
        threshold (float) -- Lowest value of distance to detect as event
            (Helps weed out changes in noise)

    Returns:
        events_at (list) -- List of indices where events occurred
    """

    if not isinstance(distance_list, list):
        raise TypeError("Expected {} got {}".format(list, type(distance_list)))

    events_at = []

    prev_distance = distance_list[0]
    curr_distance = distance_list[1]

    for index in range(2, len(distance_list)):
        next_distance = distance_list[index]

        # To find extremum, events on both sides should have lower distance
        if next_distance <= curr_distance and prev_distance <= curr_distance:

            if curr_distance >= threshold:
                # The index is for the next distance, so -1
                events_at.append(index - 1)

        prev_distance = curr_distance
        curr_distance = next_distance

    return events_at
