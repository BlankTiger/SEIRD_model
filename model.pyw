import platform
import PySimpleGUI as sg

from utils.gui import layout, layout_param, layout_stat
from utils.mathematics import solve_SEIRD
from utils.plots import plot_SEIRD
from utils.example_coefficient_matrices import sweden_coefficients
from utils.example_initial_conditions import y0_sweden
from utils.example_contact_matrices import sweden_contact_matrix
from utils.drawing import (
    draw_fig,
    delete_figure_agg,
    create_updated_fig_SEIRD,
    create_updated_fig_SEIRD_vac,
)
from utils.validation import (
    validate_positive_float_input,
    validate_positive_int_input,
)

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
fig = plot_SEIRD(sol.t, sol.y)

# Scale the GUI window to the figure DPI
set_scale(fig.dpi / 75)


sg.theme("DarkGrey5")
with_vaccinations = False

window = sg.Window(
    title="SEIRD model",
    layout=layout,
    element_justification="c",
    resizable=True,
    finalize=True,
)

# Insert initial figure into canvas
fig_agg = draw_fig(window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas)


def show_param_window():
    window = sg.Window(
        title="Parameters",
        layout=layout_param,
        element_justification="c",
        resizable=True,
        finalize=True,
    )
    params = []

    while True:
        event, values = window.read()
        if event in (None, "Exit"):
            break
        elif event == "-SAVE-":
            params = window["-PARAMTAB-"].Values
            print(params)
        elif event == "-OKAY-":
            pass


def show_stat_window():
    window = sg.Window(title="Statistics", layout=layout_stat, resizable=True)

    while True:
        event, values = window.read()
        if event in (None, "Exit"):
            break

    return


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
    elif event == "-DRAW-" and with_vaccinations:
        delete_figure_agg(fig_agg)
        if ():
            fig = create_updated_fig_SEIRD_vac()
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        else:
            sg.popup_error("Invalid input", title="Error")
    elif event == "-DRAW-":
        delete_figure_agg(fig_agg)
        if ():
            fig = create_updated_fig_SEIRD()
            fig_agg = draw_fig(
                window["-CANVAS-"].TKCanvas, fig, window["-TOOLBAR-"].TKCanvas
            )
        else:
            sg.popup_error("Invalid input", title="Error")
