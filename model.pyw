import platform
import PySimpleGUI as sg
import numpy as np

from utils.gui import layout, layout_param, layout_stat
from utils.mathematics import solve_SEIRD
from utils.plots import plot_SEIRD
from utils.example_coefficient_matrices import sweden_coefficients
from utils.example_initial_conditions import y0_sweden
from utils.example_contact_matrices import sweden_contact_matrix
from utils.drawing import draw_fig, delete_figure_agg, create_updated_fig_SEIRD
from utils.validation import validate_params, validate_params_vac, validate_positive_int


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


# Solve SEIRD model for example data of Sweden
sol = solve_SEIRD([0, 100], y0_sweden, sweden_coefficients, sweden_contact_matrix)

# Create a figure from the solution
fig = plot_SEIRD(sol.t, sol.y, sweden_coefficients, sweden_contact_matrix)

# Scale the GUI window to the figure DPI
set_scale(fig.dpi / 75)


sg.theme("DarkGrey5")

window = sg.Window(
    title="SEIRD model",
    layout=layout,
    element_justification="c",
    resizable=True,
    finalize=True,
)
sg.set_options(dpi_awareness=True)

# Insert initial figure into canvas
fig_agg = draw_fig(window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas)

parameters = {
    "-INITIALTAB-": y0_sweden,
    "-PARAMTAB-": sweden_coefficients,
    "-CONTACTTAB-": sweden_contact_matrix,
}
vac_parameters = {
    "eff": 0.9,
    "age_grp_1": [0, 0, 0],
    "age_grp_2": [0, 0, 0],
    "age_grp_3": [0, 0, 0],
    "age_grp_4": [0, 0, 0],
    "age_grp_5": [0, 0, 0],
    "age_grp_6": [0, 0, 0],
    "age_grp_7": [0, 0, 0],
    "age_grp_8": [20000, 50, 70],
}


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
    _x, _y, _width, _height = table.bbox(1, 1)
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
    # x = window.size[0] - table.winfo_rootx() + col * width
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
    global edit, params_shown, params_size, with_vac
    edit = False
    layout = layout_param(parameters, vac_parameters, with_vac)
    window = sg.Window(
        title="Parameters",
        layout=layout,
        element_justification="c",
        resizable=False,
        finalize=True,
    )

    params_shown = True
    window["-INITIALTAB-"].Widget.column("#1", anchor="center")
    window["-PARAMTAB-"].Widget.column("#1", anchor="center")
    window["-CONTACTTAB-"].Widget.column("#1", anchor="center")

    while True:
        event, values = window.read()
        if event in (None, "Exit"):
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
                    # validate_pos_under_one()
                    vac_parameters["eff"] = float(values["vaccination_eff"])
                    for i in range(1, 9):
                        age_grp = f"age_grp_{i}"
                        cur_row = vac_parameters[age_grp]
                        cur_row[0] = int(values[f"vaccination_rate_{i}"])
                        cur_row[1] = int(values[f"vaccination_start_{i}"])
                        cur_row[2] = int(values[f"vaccination_end_{i}"])
                        vac_parameters[age_grp] = cur_row
                except ValueError:
                    sg.popup_error(
                        "Vaccination eff must be a valid number, rate, start and end parameters must all be whole numbers."
                    )

        elif isinstance(event, tuple):
            row, col = event[2]
            if row is not None and col is not None:
                edit_cell(window, event[0], row + 1, col, justify="right")


def show_stat_window():
    global edit
    edit = False
    y = sol.y
    age_grp, r_n0, infectious, dead = [], [], [], []
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
        infectious.append(np.int32(max(y[2][:, i] + y[3][:, i])))
        dead.append(np.int32(max(y[5][:, i])))
    age_grp.append("Total")
    r_n0.append("")
    infectious.append("")
    dead.append(sum(dead))
    stats = np.array([age_grp, r_n0, infectious, dead]).T

    window = sg.Window(
        title="Statistics", layout=layout_stat(stats), resizable=True, finalize=True
    )

    while True:
        event, values = window.read()
        if event in (None, "Exit"):
            window.close()
            break


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
        if (
            validate_params(parameters)
            and validate_params_vac(vac_parameters)
            and validate_positive_int(values["-DURATION-"])
        ):
            fig, sol = create_updated_fig_SEIRD(
                int(values["-DURATION-"]), parameters, vac_parameters
            )
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        else:
            sg.popup_error("Invalid parameters")
    elif event == "-DRAW-":
        delete_figure_agg(fig_agg)
        if validate_params(parameters) and validate_positive_int(values["-DURATION-"]):
            fig, sol = create_updated_fig_SEIRD(int(values["-DURATION-"]), parameters)
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        else:
            sg.popup_error("Invalid parameters")
