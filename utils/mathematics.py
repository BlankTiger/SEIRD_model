from . import model_equations
import numpy as np
from dataclasses import dataclass

f = model_equations.SEIRD
SEIRD_args = model_equations.SEIRD_args


@dataclass
class solution:
    t: np.ndarray
    y: np.ndarray


def solve_SEIRD(time_range, y0, coeff, contact_matrix):

    dt = 1
    time_points = np.arange(time_range[0], time_range[1], dt)
    # have to create 48 solution place holders
    # row is values for for ex. S = |S0|S1|S2|S3|S4|S5|S6|S7|
    (S, E, Is, Ia, R, D) = (np.zeros(shape=(len(time_points), 8)) for _ in range(6))
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
            prev_y = np.array([S[t, i], E[t, i], Is[t, i], Ia[t, i], R[t, i], D[t, i]])
            sum_contact_Im = np.squeeze(np.asarray(contact_matrix[i, :])).T.dot(
                Is[t, :] + Ia[t, :]
            )
            args = SEIRD_args(
                beta[0, i],
                sigma[0, i],
                epsilon[0, i],
                f_s[0, i],
                gamma_s[0, i],
                gamma_a[0, i],
                delta[0, i],
                sum_contact_Im,
            )

            k1 = np.array(f(t, prev_y, args))
            k2 = np.array(f(t + dt2, prev_y + dt2 * k1, args))
            k3 = np.array(f(t + dt2, prev_y + dt2 * k2, args))
            k4 = np.array(f(t + dt, prev_y + dt * k3, args))
            new_y = prev_y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            S[t + 1, i] = new_y[0]
            E[t + 1, i] = new_y[1]
            Is[t + 1, i] = new_y[2]
            Ia[t + 1, i] = new_y[3]
            R[t + 1, i] = new_y[4]
            D[t + 1, i] = new_y[5]

    return solution(np.array(time_points), np.array([S, E, Is, Ia, R, D]))
