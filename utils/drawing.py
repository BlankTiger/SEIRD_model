from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)
from . import plots
from . import mathematics as mat


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


def draw_fig(canvas, fig, canvas_toolbar):
    """Draws the figure on the figure_canvas_agg

    Args:
        canvas (tk.Canvas): The canvas on which the figure is drawn
        fig (matplotlib.figure): The figure to be drawn
        canvas_toolbar (Toolbar): The toolbar of the canvas

    Returns:
        figure_canvas_agg (FigureCanvasTkAgg): The figure canvas
    """
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=True)
    return figure_canvas_agg


def delete_figure_agg(figure_canvas_agg):
    """Deletes the figure_canvas_agg content

    Args:
        figure_canvas_agg (FigureCanvasTkAgg): The figure_canvas_agg from which
            the content is deleted
    """
    for item in figure_canvas_agg.get_tk_widget().find_all():
        figure_canvas_agg.get_tk_widget().delete(item)
    figure_canvas_agg.get_tk_widget().pack_forget()


def create_updated_fig_SEIRD(
    t_1, params, params_vac=None, screen_size=None, vac_E=True
):
    y0 = params["-INITIALTAB-"]
    coeff = params["-PARAMTAB-"]
    contact = params["-CONTACTTAB-"]
    sol = mat.solve_SEIRD([0, t_1], y0, coeff, contact, params_vac, vac_E)
    t, y = sol.t, sol.y

    fig = plots.plot_SEIRD(t, y, screen_size)
    return fig, sol
