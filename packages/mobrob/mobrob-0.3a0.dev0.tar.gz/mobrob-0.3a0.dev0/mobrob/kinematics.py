#!/usr/bin/python3

import math
import numpy as np

def pose_update(x, u, DT = 0.1):
    """Pose update from input velocity (kinematic forward model).
    Returns a pose of shape (n, 3) containing [x, y, phi] position and orientation.

    Keyword arguments
    x -- current pose of shape (3, 1)
    u -- input velocity of shape (2,1)
    DT -- optional: time delta for simulation step (default value: 0.1)"""
    A = np.identity(3)
    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT]])
    x = A.dot(x) + B.dot(u)
    return x


def forward_simulation(vomega, dt = 0.1):
    """Sample a trajectory starting from zero.
    Returns a trajectory of shape (n, 3) containing [x, y, phi] position and orientation.

    Keyword arguments
    vomega -- a numpy array of shape (n, 2)"""
    xyphi = update = np.zeros((3, 1))
    for u in vomega:
        update = pose_update(update, u, dt)
        xyphi = np.hstack((xyphi, update))
    xyphi = xyphi.T
    return xyphi[0:-1]


def sample_trajectories(vomegas, dt=0.1):
    trajectories = []
    for vomega in vomegas:
        xyphi = forward_simulation(vomega, dt)
        trajectories.append(xyphi)
    return trajectories


# laserscan kinematics

def update_scan(ranges, angles, v, omega, delta_t): # delta_t in ms
    steps = int(delta_t / 100) # update in 100 ms steps -> one time-step is 0.1 seconds
    for i in range(steps):
        ranges = ranges - np.cos(angles) * v * 0.1
        angles = angles + np.sin(angles) * v * 0.1 / ranges - omega * 0.1
    return (ranges, angles)


def update_scan_trajectory(ranges, angles, v, omega, delta_t): # delta_t in ms
    steps = int(delta_t / 100) # update in 100 ms steps -> one time-step is 0.1 seconds
    for i in range(steps):
        ranges = ranges - np.cos(angles) * v[i] * 0.1
        angles = angles + np.sin(angles) * v[i] * 0.1 / ranges - omega[i] * 0.1
    return (ranges, angles)
