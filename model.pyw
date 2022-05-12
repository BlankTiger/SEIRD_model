import platform
from os import environ
from os.path import isfile
import importlib

import PySimpleGUI as sg
import numpy as np
from dataclasses import dataclass

from utils.gui import layout, layout_param, layout_stat
from utils.icon import icon
from utils.mathematics import solve_SEIRD
from utils.plots import plot_SEIRD
from utils.example_coefficient_matrices import sweden_coefficients
from utils.example_initial_conditions import y0_sweden
from utils.example_contact_matrices import sweden_contact_matrix
from utils.example_vac_params import vac_parameters
from utils.drawing import draw_fig, delete_figure_agg, create_updated_fig_SEIRD
from utils.validation import validate_params, validate_params_vac, validate_positive_int


@dataclass
class Screen:
    width: int
    height: int


if platform.system() == "Windows":
    import ctypes

    if platform.release() == "7":
        ctypes.windll.user32.SetProcessDPIAware()
    elif float(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


def set_scale(scale):
    root = sg.tk.Tk()
    root.tk.call("tk", "scaling", scale)
    root.destroy()


def get_screen_size():
    root = sg.tk.Tk()
    root.withdraw()
    screen_size = Screen(root.winfo_screenwidth(), root.winfo_screenheight())
    root.destroy()
    return screen_size


if "_PYIBoot_SPLASH" in environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash

    pyi_splash.close()

if __name__ == "__main__":
    icon = icon
else:
    icon = "icon.ico"


# Solve SEIRD model for example data of Sweden
sol = solve_SEIRD([0, 100], y0_sweden, sweden_coefficients, sweden_contact_matrix)

# Create a figure from the solution
screen_size = get_screen_size()
fig = plot_SEIRD(sol.t, sol.y, screen_size)

# Scale the GUI window to the figure DPI and screen size
if screen_size.width >= 1920:
    set_scale(fig.dpi / 75)
    font = (r"Helvetica", 12)
    font_param = (r"Helvetica", 12)
    font_stat = (r"Helvetica", 12)
    param_resizable = False
else:
    font = (r"Helvetica", 9)
    font_param = (r"Helvetica", 8)
    font_stat = (r"Helvetica", 9)
    param_resizable = False

sg.theme("DarkGrey5")
sg.set_options(dpi_awareness=True)

window = sg.Window(
    title="SEIRD model",
    icon=icon,
    layout=layout(screen_size),
    element_justification="c",
    resizable=True,
    finalize=True,
    font=font,
)

# Insert initial figure into canvas
fig_agg = draw_fig(window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas)

parameters = {
    "-INITIALTAB-": y0_sweden,
    "-PARAMTAB-": sweden_coefficients,
    "-CONTACTTAB-": sweden_contact_matrix,
}

vac_parameters = vac_parameters


def edit_cell(window, key, row, col, justify="left"):

    global edit

    def callback(event, row, col, text, key, key_tab):
        global edit
        widget = event.widget
        if key == "Return":
            text = widget.get()
        values = list(table.item(row, "values"))
        widget.destroy()
        widget.master.destroy()
        if col > 0:
            try:
                param_values[row - 1, col - 1] = float(text)
                values[col] = text
                parameters[key_tab] = param_values
            except ValueError:
                param_values[row - 1, col - 1] = float(prev_text)
                values[col] = prev_text
                parameters[key_tab] = param_values
        table.item(row, values=values)
        edit = False

    if edit or row <= 0 or col == 0:
        return

    edit = True
    root = window.TKroot
    table = window[key].Widget
    _, _y, _width, _height = table.bbox(1, 1)
    _y = table.winfo_rooty() - window["-INITIALTAB-"].Widget.winfo_rooty()

    if key == "-INITIALTAB-":
        param_values = parameters[key].astype(np.int64)
    elif key == "-PARAMTAB-":
        param_values = parameters[key].astype(np.float64)
    elif key == "-CONTACTTAB-":
        param_values = parameters[key].astype(np.float64)

    text = table.item(row, "values")[col]
    x, y, width, height = table.bbox(row, col)
    x += 2 * _width
    y += _height + _y
    height *= 0.9
    width *= 0.9

    frame = sg.tk.Frame(root)
    frame.place(x=x, y=y, width=width, height=height, anchor="nw")
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    prev_text = text
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    entry.pack()
    entry.select_range(0, sg.tk.END)
    entry.icursor(sg.tk.END)
    entry.focus_force()
    entry.bind(
        "<Return>",
        lambda e, r=row, c=col, t=text, k="Return", key=key: callback(
            e, r, c, t, k, key
        ),
    )
    entry.bind(
        "<Escape>",
        lambda e, r=row, c=col, t=text, k="Escape", key=key: callback(
            e, r, c, t, k, key
        ),
    )
    entry.bind(
        "<FocusOut>",
        lambda e, r=row, c=col, t=text, k="Return", key=key: callback(
            e, r, c, t, k, key
        ),
    )


params_shown = False
params_size = None
with_vac = False


def show_param_window():
    global edit, params_shown, params_size, with_vac, parameters, vac_parameters
    edit = False
    layout = layout_param(parameters, vac_parameters, with_vac)
    window = sg.Window(
        title="Parameters",
        icon=icon,
        layout=layout,
        element_justification="c",
        resizable=param_resizable,
        grab_anywhere=True,
        finalize=True,
        font=font_param,
    )

    params_shown = True
    window["-INITIALTAB-"].Widget.column("#1", anchor="center")
    window["-PARAMTAB-"].Widget.column("#1", anchor="center")
    window["-CONTACTTAB-"].Widget.column("#1", anchor="center")

    while True:
        event, values = window.read()
        if event in (None, "Exit", "-CLOSE-"):
            window.close()
            break

        elif event == "-WITH_VAC-":
            with_vac = values["-WITH_VAC-"]
            window["vaccination_eff"].update(disabled=not values[event])
            for i in range(1, 9):
                window[f"vaccination_rate_{i}"].update(disabled=not values[event])
                window[f"vaccination_start_{i}"].update(disabled=not values[event])
                window[f"vaccination_end_{i}"].update(disabled=not values[event])
        elif event == "-SAVE-":
            if values["-WITH_VAC-"]:
                try:
                    vac_parameters["eff"] = float(values["vaccination_eff"])
                    for i in range(1, 9):
                        age_grp = f"age_grp_{i}"
                        cur_row = vac_parameters[age_grp]
                        cur_row[0] = int(values[f"vaccination_rate_{i}"])
                        cur_row[1] = int(values[f"vaccination_start_{i}"])
                        cur_row[2] = int(values[f"vaccination_end_{i}"])
                        vac_parameters[age_grp] = cur_row
                    validate_params_vac(vac_parameters)
                except ValueError:
                    sg.popup_error(
                        "Vaccination eff must be a value between 0 and 1, rate, start and end parameters must all be non negative, whole numbers.",
                        title="Invalid vaccination parameters",
                        icon=icon,
                    )
            try:
                validate_params(parameters)
            except ValueError as e:
                sg.popup_error(
                    "Invalid parameters: " + str(e),
                    title="Invalid parameters",
                    icon=icon,
                )

        elif isinstance(event, tuple):
            row, col = event[2]
            if row is not None and col is not None:
                edit_cell(window, event[0], row + 1, col, justify="right")

        elif event == "-SAVEFILE-":
            try:
                validate_params(parameters)
                validate_params_vac(vac_parameters)
                filename = sg.popup_get_file(
                    "Save parameters to file",
                    save_as=True,
                    no_window=True,
                    icon=icon,
                    multiple_files=False,
                    file_types=(("Spreadsheet files", "*.csv"), ("All files", "*.*")),
                )
                save_to_disk(filename, parameters, vac_parameters)
            except ValueError as e:
                sg.popup_error(
                    "Invalid parameters: " + str(e),
                    title="Invalid parameters",
                    icon=icon,
                )
        elif event == "-LOADFILE-":
            filename = sg.popup_get_file(
                "Load parameters from file",
                save_as=False,
                icon=icon,
                no_window=True,
                multiple_files=False,
                file_types=(("Spreadsheet files", "*.csv"), ("All files", "*.*")),
            )
            try:
                param, vac_param = load_from_disk(filename)
            except ValueError as e:
                sg.popup_error(
                    "Invalid file format"
                    + str(e)
                    + "\n"
                    + "Please remember that this program recognizes only comma separated .csv file format. Dot is used as a decimal separator.",
                    title="Invalid file format",
                    icon=icon,
                )
                param, vac_param = None, None
            if param is not None and vac_param is not None:
                parameters = param
                vac_parameters = vac_param
                window.close()
                show_param_window()
        elif event == "-LOADDEFAULT-":
            param, vac_param = load_default()
            if param is not None and vac_param is not None:
                parameters = param
                vac_parameters = vac_param
                window.close()
                show_param_window()
            else:
                sg.popup_error(
                    "Probably corrupted executable", title="Invalid file", icon=icon
                )


def save_to_disk(file, parameters, vac_parameters):
    if file is None or file == "":
        return
    import pandas as pd

    initial_values = parameters["-INITIALTAB-"].astype(str)
    param_values = parameters["-PARAMTAB-"].astype(str)
    contact_values = parameters["-CONTACTTAB-"].astype(str)

    initial_values = np.insert(initial_values, 0, [i for i in range(1, 9)], axis=0)
    initial_value_headers = ["n", "Sn", "En", "Isn", "Ian", "Rn", "Dn"]
    initial_df = pd.DataFrame(initial_values, index=initial_value_headers)

    param_values = np.insert(
        param_values,
        0,
        [i for i in range(1, 9)],
        axis=0,
    )
    param_headers = [
        "n",
        "beta",
        "sigma",
        "epsilon",
        "fs",
        "gamma_s",
        "gamma_a",
        "delta",
    ]
    param_df = pd.DataFrame(param_values, index=param_headers)

    contact_values = np.insert(
        contact_values,
        0,
        [i for i in range(1, 9)],
        axis=1,
    )
    contact_headers = ["n", "1", "2", "3", "4", "5", "6", "7", "8"]
    contact_df = pd.DataFrame(contact_values, columns=contact_headers)

    eff_df = pd.DataFrame([[vac_parameters["eff"]]], columns=["eff"])
    eff = vac_parameters.pop("eff")

    vac_data = []
    vac_index = []
    vac_columns = ["rate", "start", "end"]
    for k, v in vac_parameters.items():
        vac_index.append(k)
        vac_data.append(v)
    vac_df = pd.DataFrame(vac_data, index=vac_index, columns=vac_columns)
    vac_parameters["eff"] = eff

    with open(file, "w", newline="\n") as f:
        initial_df.to_csv(f, index=True, header=False)
        f.write("\n")
        param_df.to_csv(f, index=True, header=False)
        f.write("\n")
        contact_df.to_csv(f, index=False, header=True)
        f.write("\n")
        eff_df.to_csv(f, index=False, header=True)
        f.write("\n")
        vac_df.to_csv(f, index=True, header=True)


def load_from_disk(file):
    try:
        if not isfile(file) or not file.lower().endswith(".csv"):
            raise FileNotFoundError
    except FileNotFoundError:
        sg.popup_error("File not found", title="Error", icon=icon)
        return None, None

    import pandas as pd

    dfs = pd.read_csv(file, header=None, dtype=str).dropna(how="all")

    initial = dfs.iloc[1:7, 1:].to_numpy(dtype=np.int64)
    param = dfs.iloc[8:15, 1:].to_numpy(dtype=np.float64)
    contact = dfs.iloc[16:24, 1:].to_numpy(dtype=np.float64)
    eff = dfs.iloc[25, :1].to_numpy(dtype=np.float64)
    vac_head = dfs.iloc[27:35, :1].to_numpy(dtype=str)
    vac_val = dfs.iloc[27:35, 1:4].to_numpy(dtype=np.int64)

    vac_params = {"eff": eff[0]}
    for i in range(len(vac_head)):
        vac_params[str(vac_head[i][0])] = vac_val[i].tolist()

    params = {
        "-INITIALTAB-": np.matrix(initial),
        "-PARAMTAB-": np.matrix(param),
        "-CONTACTTAB-": np.matrix(contact),
    }

    return params, vac_params


def load_default():
    from utils.example_initial_conditions import y0_sweden
    from utils.example_coefficient_matrices import sweden_coefficients
    from utils.example_contact_matrices import sweden_contact_matrix
    from utils.example_vac_params import vac_parameters

    params = {
        "-INITIALTAB-": y0_sweden,
        "-PARAMTAB-": sweden_coefficients,
        "-CONTACTTAB-": sweden_contact_matrix,
    }
    vac_params = vac_parameters

    return params, vac_params


def save_stats_to_disk(file, stats):
    if file is None or file == "":
        return
    import pandas as pd

    stats_headers = [
        "n",
        "R_n0",
        "max(I_sn)",
        "max(I_an)",
        "D_n(t_max)",
    ]
    stats_df = pd.DataFrame(stats, columns=stats_headers)

    with open(file, "w", newline="\n") as f:
        stats_df.to_csv(f, index=False, header=True)


def show_stat_window():
    global edit
    edit = False
    y = sol.y
    age_grp, r_n0, infectious_a, infectious_s, dead = [], [], [], [], []
    y0 = parameters["-INITIALTAB-"]
    coeff = parameters["-PARAMTAB-"]
    contact = parameters["-CONTACTTAB-"]

    S0 = y0[0].flat
    beta = coeff[0].flat
    sigma = coeff[1].flat
    fs = coeff[3].flat
    gamma_s = coeff[4].flat
    gamma_a = coeff[5].flat
    delta_n = coeff[6].flat

    for i in range(8):
        R = (
            beta[i]
            * sigma[i]
            * S0[i]
            * contact[i, i]
            * (fs[i] * gamma_a[i] + (1 - fs[i]) * (delta_n[i] + gamma_s[i]))
        ) / (gamma_a[i] * (gamma_s[i] + delta_n[i]))
        R = np.round(R, 2)
        age_grp.append(str(int(i + 1)))
        r_n0.append(R)
        infectious_s.append(np.int64(max(y[2][:, i])))
        infectious_a.append(np.int64(max(y[3][:, i])))
        dead.append(np.int32(max(y[5][:, i])))
    age_grp.append("")
    r_n0.append("")
    infectious_s.append("")
    infectious_a.append("Sum:")
    dead.append(sum(dead))
    stats = np.array([age_grp, r_n0, infectious_s, infectious_a, dead]).T

    window = sg.Window(
        title="Statistics",
        layout=layout_stat(stats),
        icon=icon,
        resizable=True,
        finalize=True,
        font=font_stat,
    )

    while True:
        event, values = window.read()
        if event in (None, "Exit"):
            window.close()
            break
        elif event == "-SAVESTATS-":
            try:
                filename = sg.popup_get_file(
                    "Save parameters to file",
                    save_as=True,
                    no_window=True,
                    icon=icon,
                    multiple_files=False,
                    file_types=(("Spreadsheet files", "*.csv"), ("All files", "*.*")),
                )
                save_stats_to_disk(filename, stats)
            except ValueError as e:
                sg.popup_error(
                    "Invalid parameters: " + str(e),
                    title="Invalid parameters",
                    icon=icon,
                )


# Main loop
while True:
    event, values = window.read()
    if event in (None, "Exit"):
        window.close()
        break
    elif event == "-PARAM-":
        show_param_window()
    elif event == "-STAT-":
        show_stat_window()
    elif event == "-DRAW-" and with_vac:
        delete_figure_agg(fig_agg)
        try:
            validate_params(parameters)
            validate_params_vac(vac_parameters)
            validate_positive_int(values["-DURATION-"], "Duration")
            fig, sol = create_updated_fig_SEIRD(
                int(values["-DURATION-"]), parameters, vac_parameters, screen_size
            )
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        except ValueError as e:
            sg.popup_error(
                "Invalid parameters: " + str(e), title="Invalid parameters", icon=icon
            )

    elif event == "-DRAW-":
        delete_figure_agg(fig_agg)
        try:
            validate_params(parameters)
            validate_positive_int(values["-DURATION-"], "Duration")
            fig, sol = create_updated_fig_SEIRD(
                int(values["-DURATION-"]), parameters, screen_size=screen_size
            )
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        except ValueError as e:
            sg.popup_error(
                "Invalid parameters: " + str(e), title="Invalid parameters", icon=icon
            )
