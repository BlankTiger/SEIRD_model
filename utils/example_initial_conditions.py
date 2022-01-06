import numpy as np


# age group n->|1|2|3|4|5|6|7|8|
# y_0
# |
# v
# S0
# E0
# Is0
# Ia0
# R0
# D0
y0_test = np.matrix(
    [
        [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4],
        [0, 1e-4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
y0_sweden = np.matrix(
    [
        [1.4e6, 1.8e6, 1.25e6, 1.5e6, 1.2e6, 1.25e6, 1.25e6, 2.0e6],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

y0_sweden_smaller = np.matrix(
    [
        [140000, 180000, 125000, 150000, 120000, 125000, 125000, 200000],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)