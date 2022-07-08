from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np


def default_display(series, scale_space, interval_tree, figsize=(10, 12)):
    """ A default display showing the series with the associated
        scale space segmentation.

        Parameters
        ----------

        series: array
            The time series.

        scale_space: dict
            The associated scale space (see utils.create_scale_space).

        interval_tree: IntervalNode
            The root node of the interval tree (see interval_tree).

        Returns
        -------

        fig: matplotlib figure
    """
    # Display the image and plot all contours found
    fig, ax = plt.subplots(1, 2, figsize=figsize, sharey=True)
    tune = 1

    ax[0].plot(series, np.arange(len(series)))

    extent = [0, 50, len(series) - 1, 0]
    ax[1].imshow(
        scale_space["second"],
        aspect='auto',
        vmin=-tune,
        vmax=tune,
        cmap='seismic',
        extent=extent,
        alpha=1)

    contour_list = interval_tree["contour_list"]
    for contour in contour_list:
        ax[1].plot(
            contour['data'][:, 1], contour['data'][:, 0], linewidth=1, alpha=1)

    rect_list = interval_tree["root"].preOrderTraversal(interval_tree["root"])
    for rect in rect_list:
        bottom = rect['bottom']
        top = rect['top']
        scale = rect['scale']
        rect = Rectangle(
            (0, top), scale, bottom-top, linewidth=1, edgecolor='k',
            fill=False)
        ax[1].add_patch(rect)

    return fig
