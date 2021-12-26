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
        f_sn (float): The fraction of infected people who are symptomatic.
        gamma_sn (float): The recovery rate of symptomatic infected people.
        gamma_an (float): The recovery rate of asymptomatic infected people.
        delta_n (float): The death rate of symptomatic infected people.
        sum_m_contact_nm_times_I_m (float): The sum of a product of the contact
            between age group n and m and the number of infected people in age
            group m.

    Returns:


    """

    S_n, E_n, I_sn, I_an, R_n, D_n = y

    Sn = -beta_n * sigma_n * S_n * sum_m_contact_nm_times_I_m
    En = beta_n * sigma_n * S_n * sum_m_contact_nm_times_I_m - sigma_n * E_n
    Isn = epsilon_n * f_sn * E_n - (gamma_sn + delta_n) * I_sn
    Ian = epsilon_n * (1 - f_sn) * E_n - gamma_an * I_an
    Rn = gamma_an * I_an + gamma_sn * I_sn
    Dn = delta_n * I_sn

    dydt = [Sn, En, Isn, Ian, Rn, Dn]
    return dydt
