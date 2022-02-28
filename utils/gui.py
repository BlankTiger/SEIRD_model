import PySimpleGUI as sg


with_vaccinations = False
sg.theme("DarkGrey5")


def create_stretch():
    """Create a stretch element

    Returns:
        sg.Text: stretch element for layout
    """
    return sg.Text(
        font="_ 1", text="", background_color=None, pad=(0, 0), expand_x=True
    )


def create_col_for_row(elem):
    """Create a column for a row

    Args:
        elem (sg.Element): element to be placed in the column

    Returns:
        sg.Column: column for a row
    """
    return sg.Column([[elem]], pad=(0, 0))


def create_row(col_1, col_2, col_3, row_visible, row_key=""):
    """Create a row


    Args:
        col_1 (sg.Column): first column of the row
        col_2 (sg.Column): second column of the row
        col_3 (sg.Column): third column of the row
        row_visible (bool): whether the row is visible or not
        row_key (str): key of the row

    Returns:
        sg.Column: row
    """
    return sg.Column(
        [[create_stretch(), col_1, col_2, col_3, create_stretch()]],
        pad=(0, 0),
        key=row_key,
        visible=row_visible,
        expand_x=True,
    )


def create_layout(*elements):
    """Create a layout


    Args:
        *elements (sg.Element): elements to be placed in the layout

    Returns:
        list: layout
    """
    return [[*elements]]


param_row = create_row(
    create_stretch(),
    sg.Button("Parameters", key="-PARAM-", size=(12, 2), expand_x=True),
    create_stretch(),
    True,
)

stat_row = create_row(
    create_stretch(),
    sg.Button("Statistics", key="-STAT-", size=(12, 2), expand_x=True),
    create_stretch(),
    True,
)

draw_row = create_row(
    create_stretch(),
    sg.Button("Plot", key="-DRAW-", size=(12, 2), expand_x=True),
    create_stretch(),
    True,
)


column1 = sg.Column(
    [
        [param_row],
        [create_stretch()],
        [stat_row],
        [create_stretch()],
        [draw_row],
    ],
    justification="left",
    element_justification="c",
    expand_x=True,
)

column2 = sg.Column(
    [
        [
            sg.Canvas(
                key="-CANVAS-",
                background_color="white",
                expand_y=True,
                expand_x=True,
                size=(1300, 800),
            )
        ],
        [
            sg.Canvas(
                key="-TOOLBAR-",
                background_color="white",
                size=(1300, 20),
                expand_x=True,
                expand_y=False,
            )
        ],
    ],
    expand_y=True,
    expand_x=True,
)


# Create the param window layout
from utils.example_initial_conditions import y0_sweden
from utils.example_coefficient_matrices import sweden_coefficients
from utils.example_contact_matrices import sweden_contact_matrix
import numpy as np

y0_sweden = y0_sweden.astype(str)
sweden_coefficients = sweden_coefficients.astype(str)
sweden_contact_matrix = sweden_contact_matrix.astype(str)

left_headings = np.array(
    [
        [
            "S(0)ₙ",
            "E(0)ₙ",
            "I(0)ₐ,ₙ",
            "I(0)ₛ,ₙ",
            "R(0)ₙ",
            "D(0)ₙ",
        ]
    ]
)
y0_sweden = np.insert(y0_sweden, 0, left_headings, axis=1)

left_headings = np.array(
    [
        [
            "β ₙ",
            "σ ₙ",
            "ε ₙ",
            "f ₛ,ₙ",
            "γ ₛ,ₙ",
            "γ ₐ,",
            "δ ₙ",
        ]
    ]
)
sweden_coefficients = np.insert(sweden_coefficients, 0, left_headings, axis=1)

left_headings = np.array(
    [
        [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
        ]
    ]
)
sweden_contact_matrix = np.insert(sweden_contact_matrix, 0, left_headings, axis=1)

vertical_scroll = False
initial_conditions_table = sg.Table(
    y0_sweden.tolist(),
    headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
    hide_vertical_scroll=vertical_scroll,
    row_height=35,
    key="-INITIALTAB-",
    num_rows=6,
    expand_x=True,
    font=(r"Helvetica 11"),
)

coefficient_table = sg.Table(
    sweden_coefficients.tolist(),
    headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
    hide_vertical_scroll=vertical_scroll,
    row_height=35,
    key="-PARAMTAB-",
    num_rows=7,
    expand_x=True,
    font=(r"Helvetica 11"),
)

contact_table = sg.Table(
    sweden_contact_matrix.tolist(),
    headings=["n", "1", "2", "3", "4", "5", "6", "7", "8"],
    hide_vertical_scroll=vertical_scroll,
    row_height=35,
    key="-CONTACTTAB-",
    num_rows=8,
    expand_x=True,
    font=(r"Helvetica 11"),
)
param_buttons = sg.Column(
    [[sg.Button("Save", key="-SAVE-", size=(12, 2))]], expand_x=True
)

main_frame = sg.Column(
    [
        [sg.Text("Initial conditions:"), create_stretch()],
        [initial_conditions_table],
        [sg.Text("Coefficients:"), create_stretch()],
        [coefficient_table],
        [sg.Text("Contact matrix:"), create_stretch()],
        [contact_table],
    ],
    element_justification="c",
    expand_x=True,
    expand_y=True,
)

layout = create_layout(column1, column2)
layout_param = create_layout(param_buttons, main_frame)
layout_stat = create_layout()
