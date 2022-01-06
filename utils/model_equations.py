from numpy import array


def SEIRD(
    t,
    y,
    beta_n,
    sigma_n,
    epsilon_n,
    f_sn,
    gamma_sn,
    gamma_an,
    delta_n,
    sum_m_contact_nm_times_I_m,
):
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

    dIsndt = epsilon_n * f_sn * E_n - (gamma_sn + delta_n) * I_sn
    dIandt = epsilon_n * (1 - f_sn) * E_n - gamma_an * I_an
    dRndt = gamma_an * I_an + gamma_sn * I_sn
    dDndt = delta_n * I_sn

    if S_n - beta_n * sigma_n * S_n * sum_m_contact_nm_times_I_m > 0:
        dSndt = -beta_n * sigma_n * S_n * sum_m_contact_nm_times_I_m
        dEndt = (
            beta_n * sigma_n * S_n * sum_m_contact_nm_times_I_m
            - epsilon_n * E_n
        )
        return array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])

    dSndt = -S_n
    dEndt = S_n - epsilon_n * E_n

    return array([dSndt, dEndt, dIsndt, dIandt, dRndt, dDndt])
