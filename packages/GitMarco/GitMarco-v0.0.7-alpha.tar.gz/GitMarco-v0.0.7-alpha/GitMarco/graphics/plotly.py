import plotly.graph_objects as go
import numpy as np


class Scatter3D(object):
    def __init__(self,
                 x: np.ndarray,
                 y: np.ndarray,
                 z: np.ndarray, ):
        """
        :param x: np.ndarray - data are reshaped with (-1, 1)
        :param y: np.ndarray - data are reshaped with (-1, 1)
        :param z: np.ndarray - data are reshaped with (-1, 1)

        Create a 3D scatter plot with plotly
        """
        self.x = x
        self.y = y
        self.z = z
        self.grid = np.hstack((self.x.reshape(-1, 1),
                               self.y.reshape(-1, 1),
                               self.z.reshape(-1, 1)))

    def plot(self,
             color: np.ndarray = None,
             title: str = '',
             xlabel: str = '',
             ylabel: str = '',
             legend_title: str = '',
             size: tuple = (800, 600),
             show: bool = False):
        """
        :param color: nodal values for the color scale
        :param title: figure title
        :param xlabel: xlabel
        :param ylabel: ylabel
        :param legend_title: legend_title
        :param size: size of the figure
        :param show: show (or not) the figure
        :return:

        Create the 3d scatter plot
        """
        color = color.reshape(-1, 1) if color is not None else color
        fig = go.Figure(data=[go.Scatter3d(x=self.x, y=self.y, z=self.z,
                                           mode='markers',
                                           marker=dict(size=5,
                                                       color=color,
                                                       colorscale='Turbo',
                                                       opacity=0.8,
                                                       colorbar=dict(thickness=20),
                                                       # line=dict(width=0.5,
                                                       #          color='black')
                                                       ))],
                        layout=go.Layout(
                            width=size[0],
                            height=size[1],
                        ))

        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            legend_title=legend_title
        )
        fig.show() if show else None
        return fig
