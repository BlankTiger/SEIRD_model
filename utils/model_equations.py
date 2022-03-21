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
    """The SEIRD model."""
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
