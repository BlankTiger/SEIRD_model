from utils.example_coefficient_matrices import (
    sweden_coefficients as sweden_coeff,
)
from utils.example_initial_conditions import y0_sweden
from utils.example_contact_matrices import (
    sweden_contact_matrix,
)
from utils.mathematics import solve_SEIRD
from utils.example_plots import cmp_age_group_sol
from utils.example_plots import all_sol_in_grid


solutions = solve_SEIRD((0, 100), y0_sweden, sweden_coeff, sweden_contact_matrix, 1)

cmp_age_group_sol(solutions)
all_sol_in_grid(solutions)
