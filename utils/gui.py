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

layout = create_layout(column1, column2)
