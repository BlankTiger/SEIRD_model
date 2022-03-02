from numpy import array
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


def SEIRD(t, y, c: SEIRD_args):
    """
    The SEIRD model.
    """
    S_n, E_n, I_sn, I_an, R_n, D_n = y

    dIsndt = c.epsilon_n * c.f_sn * E_n - (c.gamma_sn + c.delta_n) * I_sn
    dIandt = c.epsilon_n * (1 - c.f_sn) * E_n - c.gamma_an * I_an
    dRndt = c.gamma_an * I_an + c.gamma_sn * I_sn
    dDndt = c.delta_n * I_sn

    if S_n - c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m > 0:
        dSndt = -c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m
        dEndt = (
            c.beta_n * c.sigma_n * S_n * c.sum_m_contact_nm_times_I_m
            - c.epsilon_n * E_n
        )
        return array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])

    dSndt = -S_n
    dEndt = S_n - c.epsilon_n * E_n

    return array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])
