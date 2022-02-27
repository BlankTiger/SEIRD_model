from numpy import array


class SEIRD_args:
    def __init__(
        self,
        beta_n,
        sigma_n,
        epsilon_n,
        f_sn,
        gamma_sn,
        gamma_an,
        delta_n,
        sum_m_contact_nm_times_I_m,
    ):
        self.beta_n = beta_n
        self.sigma_n = sigma_n
        self.epsilon_n = epsilon_n
        self.f_sn = f_sn
        self.gamma_sn = gamma_sn
        self.gamma_an = gamma_an
        self.delta_n = delta_n
        self.sum_m_contact_nm_times_I_m = sum_m_contact_nm_times_I_m


def SEIRD(t, y, c: SEIRD_args):
    """
    The SEIRD model.

    Args:
        t (float): The time.
        y (list): The state variables.
        beta_n (float): The infection rate.
        sigma_n (float): The recovery rate.
        epsilon_n (float): The self-quarantine rate.
        f_sn (float): The fraction of infectious people who are symptomatic.
        gamma_sn (float): The recovery rate of symptomatic infectious people.
        gamma_an (float): The recovery rate of asymptomatic infectious people.
        delta_n (float): The death rate of symptomatic infectious people.
        sum_m_contact_nm_times_I_m (float): The sum of a product of the contact
            between age group n and m and the number of infectious people in
            age group m.

    Returns:


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
