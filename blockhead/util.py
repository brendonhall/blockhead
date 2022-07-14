import logging
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.stats import norm

from blockhead.interval_tree import get_parent_interval, IntervalNode


def create_scale_space(series, min_scale=3, max_scale=50):
    """ Create a scale space representation of the time series.

        Parameters
        ----------

        series: array
            A timeseries to compute the scale space over.
        min_scale: int
            The min scale in the scale space (in samples).
        max_scale: int
            The max scale in the scale space (in samples).

        Returns
        -------

        scale_space: dict
            scales: the scale (in samples).

            And the second, third order gradients of a smoothed series used to
            find the segmentation of the signal. There will be one set of
            gradients for each scale.
    """
    # FIXME - more efficient to filter multiple series at once
    if(len(series) < 4):
        raise RuntimeError("Too few data to segment the series.")

    max_scale = min(len(series), max_scale)

    scales = np.logspace(0, min_scale, max_scale)

    second_order = [
        gaussian_filter(series, i, 2, mode='reflect') for i in scales]
    third_order = [
        gaussian_filter(series, i, 3, mode='reflect') for i in scales]

    return {"scales": scales,
            "second": np.vstack(second_order).T,
            "third": np.vstack(third_order).T}


def populate_interval_tree(contours):
    """ Populate an interval tree with the contours.

    Parameters
    ----------
    contours: list(array)
        Each element in the list should be a 2-d array
        tracing out the contour in the scale space.

    Returns
    -------
    output:dict, keys are:

    "root": IntervalNode
        The root node of the interval tree.
    "contour_list": IntervalNode
        The list of contours.
    """

    max_scales = []
    top_locations = []
    bottom_locations = []
    contour_id = []
    contour_list = []

    for i, contour in enumerate(contours):
        max_scale = np.max(contour[:, 1])
        locations = contour[contour[:, 1] == 0.][:, 0]
        if len(locations) == 2:
            [location1, location2] = np.sort(locations)
        else:
            location1 = locations[0]
            location2 = None

        max_scales.append(max_scale)
        top_locations.append(location1)
        bottom_locations.append(location2)
        contour_id.append(i)

        contour_list.append({
            'max_scale': max_scale,
            'location1': location1,
            'location2': location2,
            'id': i,
            'data': contour
        })

    contour_list = sorted(
        contour_list, key=lambda d: d['max_scale'], reverse=True)

    #  root is intended to node contains all other contours:
    root_scale = max(max_scales) + 1
    root_location1 = 0
    root_location2 = max(
        max([i + 1 for i in bottom_locations if i is not None]),
        max([i + 1 for i in top_locations if i is not None])
    )

    root = IntervalNode(
        root_scale, root_location1, root_location2, None)

    for i, contour in enumerate(contour_list):
        logging.info(
            f"Adding contour {i} with scale: {contour['max_scale']:.1f}, top: {contour['location1']:.1f}, bottom: {contour['location2'] if contour['location2'] else np.nan:.1f}")  # noqa
        parent_node = get_parent_interval(root, contour)
        parent_top, parent_bottom = parent_node.get_interval()

        if contour['location2']:
            first_segment = IntervalNode(
                contour['max_scale'],
                parent_top,
                contour['location1'],
                contour)

            second_segment = IntervalNode(
                contour['max_scale'],
                contour['location1'],
                contour['location2'],
                contour)

            third_segment = IntervalNode(
                contour['max_scale'],
                contour['location2'],
                parent_bottom,
                contour)

            parent_node.add_child(first_segment)
            parent_node.add_child(second_segment)
            parent_node.add_child(third_segment)
        else:
            first_segment = IntervalNode(
                contour['max_scale'],
                parent_top,
                contour['location1'],
                contour)

            second_segment = IntervalNode(
                contour['max_scale'],
                contour['location1'],
                parent_bottom,
                contour)

            parent_node.add_child(first_segment)
            parent_node.add_child(second_segment)

    # FIXME - the contour list should be derivable from the
    # interval tree.
    return {"root": root, "contour_list": contour_list}


def default_synthetic():
    """ Generate a default time series for blocking.

    Returns
    -------
    series: array
        A timeseries with blocks.
    """
    np.random.seed(201)

    T = 1024

    big_shock = 4
    med_shock = 2
    small_shock = 1

    def arma22(N, alpha, beta, rnd, eps=0.5):
        inov = rnd.rvs(2*N)
        x = np.zeros(2*N)

        # arma22 mode
        mean = 0.0
        for i in range(2, N*2):
            rnd = np.random.rand()
            sig = 1 if np.random.rand() > 0.5 else -1
            if(rnd > 0.997):
                mean += sig * big_shock
            elif(rnd > 0.995):
                mean += sig * med_shock
            elif(rnd > 0.990):
                mean += sig * small_shock
            # else do nothing

            x[i] = mean + (
                   alpha[0] * x[i-1] + alpha[1]*x[i-2] +
                   beta[0] * inov[i-1] + beta[1] * inov[i-2] + eps * inov[i])

        result = x[N:]
        return result - np.mean(result)

    alpha = [0.95, -0.5]
    beta = [0.4, 0.0]
    eps = 0.1

    return arma22(T, alpha, beta, norm(1.0), eps=eps)
