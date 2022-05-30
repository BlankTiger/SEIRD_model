import numpy as np
from dataclasses import dataclass


@dataclass
class SEIRD_args:
    beta_n: float
    sigma_n: float
    epsilon_n: float
    f_sn: float
    gamma_sn: float
    gamma_an: float
    delta_n: float
    sum_m_contact_nm_times_I_m: float
    vac_params: list


def SEIRD(t, y, c: SEIRD_args):
    """The SEIRD model. Only S group is vaccinated."""
    diff_v = c.vac_params[0] * c.vac_params[1]
    S_n, E_n, I_sn, I_an, R_n, D_n = y

    if S_n - c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m - diff_v < 0:
        diff_v = S_n

    dSndt = -c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m - diff_v
    dEndt = (
        c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m - c.epsilon_n * E_n
    )
    dIsndt = c.epsilon_n * c.f_sn * E_n - (c.gamma_sn + c.delta_n) * I_sn
    dIandt = c.epsilon_n * (1 - c.f_sn) * E_n - c.gamma_an * I_an
    dRndt = c.gamma_an * I_an + c.gamma_sn * I_sn + diff_v
    dDndt = c.delta_n * I_sn

    return np.array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])


def SEIRD_SE(t, y, c: SEIRD_args):
    """The SEIRD model. SE groups are vaccinated."""
    S_n, E_n, I_sn, I_an, R_n, D_n = y
    diff_v = c.vac_params[0] * c.vac_params[1]

    if diff_v != 0 and S_n / (S_n + E_n) < 1:
        vac_S = diff_v * S_n / (S_n + E_n)
        vac_E = diff_v * E_n / (S_n + E_n)
    else:
        vac_S = 0
        vac_E = 0
        diff_v = 0

    corr = 0
    if S_n - c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m - vac_S < 0:
        corr = S_n

    dSndt = -c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m - vac_S - corr

    if (
        c.epsilon_n * E_n + vac_E
        > E_n + c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m
    ):
        corr = E_n
    dEndt = (
        c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m
        - c.epsilon_n * E_n
        - vac_E
        - corr
    )
    dIsndt = c.epsilon_n * c.f_sn * E_n - (c.gamma_sn + c.delta_n) * I_sn
    dIandt = c.epsilon_n * (1 - c.f_sn) * E_n - c.gamma_an * I_an
    dRndt = c.gamma_an * I_an + c.gamma_sn * I_sn + diff_v
    dDndt = c.delta_n * I_sn

    return np.array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])
