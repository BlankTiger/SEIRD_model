from .model_equations import SEIRD
from scipy.integrate import solve_ivp


def solve_SEIRD(
    t_range,
    y0,
    beta_n,
    sigma_n,
    epsilon_n,
    f_sn,
    gamma_sn,
    gamma_an,
    delta_n,
    sum_m_contact_nm_times_I_m,
    t_values,
):
    """Solves the SEIRD model using the scipy.integrate.solve_ivp function.

    Args:
        t_range (tuple): The time range of the simulation.
        y0 (tuple): The initial conditions.
        beta_n (float): The infection rate.
        sigma_n (float):
        epsilon_n (float):
        f_sn (float): The fraction of infectious people who are symptomatic.
        gamma_sn (float): The recovery rate of symptomatic infectious people.
        gamma_an (float): The recovery rate of asymptomatic infectious people.
        delta_n (float): The death rate of symptomatic infectious people.
        sum_m_contact_nm_times_I_m (float): The sum of a product of the contact
            between age group n and m and the number of infectious people in age
            group m.

    Returns:
        tuple: The solution of the SEIRD model.
    """
    return solve_ivp(
        SEIRD,
        t_range,
        y0,
        t_eval=t_values,
        args=(
            beta_n,
            sigma_n,
            epsilon_n,
            f_sn,
            gamma_sn,
            gamma_an,
            delta_n,
            sum_m_contact_nm_times_I_m,
        ),
    )
