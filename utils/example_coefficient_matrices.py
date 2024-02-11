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
# 7: 70-
range_8 = range(8)
beta_by_age_group = np.array([6e-6 for _ in range_8])
sigma_by_age_group = np.array([1, 1, 1, 1, 1, 1, 0.1, 0.01])
epsilon_by_age_group = np.array([0.18 for _ in range_8])
f_s_by_age_group = np.array([0.6 for _ in range_8])
gamma_s_by_age_group = np.array([0.07 for _ in range_8])
gamma_a_by_age_group = np.array([0.06 for _ in range_8])
delta_by_age_group = np.array(
    [2.8e-7, 2e-6, 5e-6, 8.58e-6, 2.22e-5, 7.58e-5, 3.4e-4, 18.7e-4]
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
    ],
    dtype=np.float64,
)
