#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt

def plot_coordinate_frame(x=0, y=0, phi=0):
    plt.text( 0.1,  0.2, "x", fontsize=12)
    plt.text(-0.2, -0.3, "y", fontsize=12)
    plt.arrow(0, 0,  0,    0.25, width = 0.005)
    plt.arrow(0, 0, -0.25, 0, width = 0.005)


def xy_plot(x, y, col="bo"):
    """Used to make a plot in x- and y-coordinates with x axis up and y axis to the left.
    Matplotlib usually: x to the right, y up."""
    plt.plot(-y, x, col)
    plot_coordinate_frame()


def plot_laserscan_xy(x, y, col="bo"): # used for pointclouds in cartesian coordinates
    xy_plot(x, y, col)
    plt.axis('equal')


def plot_laserscan_ranges(ranges, angles, col="bo"): # polar coordinates
    x = np.cos(angles)*ranges
    y = np.sin(angles)*ranges
    plot_laserscan_xy(x, y, col)


def plot_laserscan_xy_first_last(x, y, col="bo"): # used for pointclouds in cartesian coordinates
    xy_plot(x, y, col)
    xy_plot(x[0], y[0], 'ro')
    print(f"First value in red.")
    xy_plot(x[-1], y[-1], 'yo')
    print(f"Last value in yellow.")
    plt.axis('equal')
