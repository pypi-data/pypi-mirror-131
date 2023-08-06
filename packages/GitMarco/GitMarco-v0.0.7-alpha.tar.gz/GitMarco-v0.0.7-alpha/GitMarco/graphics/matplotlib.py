import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


def validation_plot(
        true: np.ndarray,
        pred: np.ndarray,
        size: tuple = (6, 6),
        title: str = '',
        show: bool = False,
        xlabel: str = 'x',
        ylabel: str = 'y',
        marker_color: str = 'b',
        edge_color: str = 'k',
        line_color: str = 'k',

):
    true = true.reshape(-1 , 1) if isinstance(true, np.ndarray) else None
    pred = pred.reshape(-1, 1) if isinstance(pred, np.ndarray) else None
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=size)
    ax.scatter(true, pred, c=marker_color, edgecolor=edge_color)
    min_ = min((min(true), min(pred)))
    max_ = max((max(true), max(pred)))
    plt.plot([min_, max_], [min_, max_], '-.', c=line_color, linewidth=0.5)
    ax.set_title(f'{title} - R2: {r2_score(true, pred)}')
    ax.set_xlim(min_, max_)
    ax.set_ylim(min_, max_)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid('both')
    plt.show() if show else None
    return fig
