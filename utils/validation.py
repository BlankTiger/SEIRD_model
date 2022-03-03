import numpy as np


def validate_params(params):
    """
    Validates the parameters passed to the script.
    """
    if params["-INITIALTAB-"].dtype != np.int64:
        raise ValueError("Initial values must be whole numbers.")
    if params["-PARAMTAB-"].dtype != np.float64:
        raise ValueError("Parameters must be a floating point numbers.")
    if params["-CONTACTTAB-"].dtype != np.float64:
        raise ValueError("Contact values must be a floating point numbers.")
    for x in params["-INITIALTAB-"].flat:
        if x < 0:
            raise ValueError("Initial values must be positive numbers.")
    for x in params["-PARAMTAB-"].flat:
        if x < 0:
            raise ValueError("Parameters must be positive numbers.")
    for x in params["-CONTACTTAB-"].flat:
        if x < 0:
            raise ValueError("Contact values must be positive numbers.")
    return True


def validate_params_vac(vac_params):
    if not isinstance(vac_params["eff"], float):
        raise ValueError("Vaccination efficiency must be a floating point number.")
    if vac_params["eff"] < 0 or vac_params["eff"] > 1:
        raise ValueError("Vaccination efficiency must be between 0 and 1.")
    for i in range(1, 9):
        grp = f"age_grp_{i}"
        if (
            not isinstance(vac_params[grp][0], int)
            or not isinstance(vac_params[grp][1], int)
            or not isinstance(vac_params[grp][2], int)
        ):
            raise ValueError(
                "All values like vaccination rate, start day, end day must be whole numbers."
            )
        if vac_params[grp][0] < 0 or vac_params[grp][1] < 0 or vac_params[grp][2] < 0:
            raise ValueError(
                "All values like vaccination rate, start day, end day must be positive numbers."
            )
    return True


def validate_positive_int(value):
    try:
        value = int(value)
        if value < 0:
            raise ValueError
        return True
    except ValueError:
        return False
