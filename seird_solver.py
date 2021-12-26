import numpy as np
from utils.model_equations import SEIRD
from utils.example_coefficient_matrices import (
    sweden_coefficients as sweden_coeff,
)
from utils.example_contact_matrices import sweden_contact_matrix


def sum_m_contact_nm_times_I_m(contact_nm, I_m):
    return contact_nm.dot(I_m)


def solve(f, time_range, y0, coeff, contact_matrix, dt):

    time_points = np.arange(time_range[0], time_range[1], dt)
    # have to create 48 solution place holders
    # row is values for for ex. S = |S0|S1|S2|S3|S4|S5|S6|S7|
    (S, E, Is, Ia, R, D) = (
        np.zeros(shape=(len(time_points), 8)) for _ in range(6)
    )
    S[0, :] = y0[0, :]
    E[0, :] = y0[1, :]
    Is[0, :] = y0[2, :]
    Ia[0, :] = y0[3, :]
    R[0, :] = y0[4, :]
    D[0, :] = y0[5, :]

    beta = coeff[0, :]
    sigma = coeff[1, :]
    epsilon = coeff[2, :]
    f_s = coeff[3, :]
    gamma_s = coeff[4, :]
    gamma_a = coeff[5, :]
    delta = coeff[6, :]

    # for each time point
    for t in range(len(time_points) - 1):
        # for each age group, all 6 diff eqs advance at once
        for i in range(8):

            dt2 = dt / 2
            prev_y = np.array(
                [
                    S[t, i],
                    E[t, i],
                    Is[t, i],
                    Ia[t, i],
                    R[t, i],
                    D[t, i],
                ]
            )
            # implement the sum argument
            sum_contact_Im = sum_m_contact_nm_times_I_m(
                np.squeeze(np.asarray(contact_matrix[i, :])).T,
                Is[t, :] + Ia[t, :],
            )
            k1 = np.array(
                f(
                    t,
                    prev_y,
                    beta[0, i],
                    sigma[0, i],
                    epsilon[0, i],
                    f_s[0, i],
                    gamma_s[0, i],
                    gamma_a[0, i],
                    delta[0, i],
                    sum_contact_Im,
                )
            )
            k2 = np.array(
                f(
                    t + dt2,
                    prev_y + dt2 * k1,
                    beta[0, i],
                    sigma[0, i],
                    epsilon[0, i],
                    f_s[0, i],
                    gamma_s[0, i],
                    gamma_a[0, i],
                    delta[0, i],
                    sum_contact_Im,
                )
            )
            k3 = np.array(
                f(
                    t + dt2,
                    prev_y + dt2 * k2,
                    beta[0, i],
                    sigma[0, i],
                    epsilon[0, i],
                    f_s[0, i],
                    gamma_s[0, i],
                    gamma_a[0, i],
                    delta[0, i],
                    sum_contact_Im,
                )
            )
            k4 = np.array(
                f(
                    t + dt,
                    prev_y + dt * k3,
                    beta[0, i],
                    sigma[0, i],
                    epsilon[0, i],
                    f_s[0, i],
                    gamma_s[0, i],
                    gamma_a[0, i],
                    delta[0, i],
                    sum_contact_Im,
                )
            )
            new_y = prev_y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            S[t + 1, i] = new_y[0]
            E[t + 1, i] = new_y[1]
            Is[t + 1, i] = new_y[2]
            Ia[t + 1, i] = new_y[3]
            R[t + 1, i] = new_y[4]
            D[t + 1, i] = new_y[5]

    return (time_points, S, E, Is, Ia, R, D)


# n->|1|2|3|4|5|6|7|8|
# m
# |
# v
# S0
# E0
# Is0
# Ia0
# R0
# D0
y0 = np.matrix(
    [
        [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4],
        [0, 1e-4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
y0_big = np.matrix(
    [
        [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [100, 0, 0, 0, 0, 0, 0, 0],
        [0, 10, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)


solutions = solve(
    SEIRD, (0, 300), y0_big, sweden_coeff, sweden_contact_matrix, 0.1
)


import matplotlib.pyplot as plt

fig, axs = plt.subplots(8, 6, sharex=True)
axs.flatten()
fig.set_size_inches(19, 19)
plt.autoscale()
for i in range(8):
    for j in range(6):
        axs[i, j].plot(solutions[0], solutions[j + 1][:, i])
plt.tight_layout()
plt.savefig("sweden_SEIRD.png", bbox_inches="tight")
print(solutions[1].shape)
