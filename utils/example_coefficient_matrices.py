import numpy as np

# age groups:
# (number corresponds to index in arrays written below)
# 0: 0-10
# 1: 10-20
# 2: 20-30
# 3: 30-40
# 4: 40-50
# 5: 50-60
# 6: 60-70
# 7: 70-80

beta_by_age_group = np.array(
    [0.25e-4, 0.25e-4, 0.25e-4, 0.25e-4, 0.25e-4, 0.25e-4, 0.25e-4, 0.25e-4]
)
sigma_by_age_group = np.array([1, 1, 1, 1, 1, 1, 1, 1])
epsilon_by_age_group = np.array(
    [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18]
)
f_s_by_age_group = np.array([0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
gamma_s_by_age_group = np.array(
    [0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07]
)
gamma_a_by_age_group = np.array(
    [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
)
delta_by_age_group = np.array(
    [0.0017, 0.0000, 0.0007, 0.0012, 0.0031, 0.0105, 0.0459, 0.3253]
)

sweden_coefficients = np.matrix(
    [
        beta_by_age_group,
        sigma_by_age_group,
        epsilon_by_age_group,
        f_s_by_age_group,
        gamma_s_by_age_group,
        gamma_a_by_age_group,
        delta_by_age_group,
    ]
)
