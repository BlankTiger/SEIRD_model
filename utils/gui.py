import PySimpleGUI as sg


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


duration_text = sg.Text("Duration in days:", size=(12, 1), expand_x=True)
duration_input = sg.InputText(
    "100", key="-DURATION-", size=(12, 1), justification="right", expand_x=True
)
duration_text_row = create_row(create_stretch(), duration_text, create_stretch(), True)
duration_input_row = create_row(
    create_stretch(), duration_input, create_stretch(), True
)

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
        [duration_text_row],
        [duration_input_row],
        [create_stretch()],
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
from utils.example_vac_params import vac_parameters
import numpy as np

params = {
    "-INITIALTAB-": y0_sweden,
    "-PARAMTAB-": sweden_coefficients,
    "-CONTACTTAB-": sweden_contact_matrix,
}
vac_parameters = vac_parameters

layout = create_layout(column1, column2)


def layout_param(parameters=params, vac_parameters=vac_parameters, with_vac=False):
    vertical_scroll = True
    y0_sweden = parameters["-INITIALTAB-"].astype(str)
    sweden_coefficients = parameters["-PARAMTAB-"].astype(str)
    sweden_contact_matrix = parameters["-CONTACTTAB-"].astype(str)

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
                "γ ₐ,ₙ",
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

    def_col_width = 10
    initial_conditions_table = sg.Table(
        y0_sweden.tolist(),
        headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=35,
        def_col_width=def_col_width,
        auto_size_columns=False,
        key="-INITIALTAB-",
        num_rows=6,
        expand_x=True,
        font=(r"Helvetica 12"),
        enable_click_events=True,
    )

    coefficient_table = sg.Table(
        sweden_coefficients.tolist(),
        headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=35,
        def_col_width=def_col_width,
        auto_size_columns=False,
        key="-PARAMTAB-",
        num_rows=7,
        expand_x=True,
        font=(r"Helvetica 12"),
        enable_click_events=True,
    )

    contact_table = sg.Table(
        sweden_contact_matrix.tolist(),
        headings=["n", "1", "2", "3", "4", "5", "6", "7", "8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=35,
        def_col_width=def_col_width,
        auto_size_columns=False,
        key="-CONTACTTAB-",
        num_rows=8,
        expand_x=True,
        font=(r"Helvetica 12"),
        enable_click_events=True,
    )
    param_buttons = sg.Column(
        [
            [
                sg.Checkbox(
                    "Vaccinations on/off",
                    default=with_vac,
                    key="-WITH_VAC-",
                    enable_events=True,
                )
            ],
            [sg.Button("Save", key="-SAVE-", size=(12, 2))],
            [create_stretch()],
            [sg.Button("Save to file", key="-SAVEFILE-", size=(12, 2))],
            [create_stretch()],
            [sg.Button("Load from file", key="-LOADFILE-", size=(12, 2))],
            [create_stretch()],
            [sg.Button("Load default", key="-LOADDEFAULT-", size=(12, 2))],
            [create_stretch()],
            [sg.Button("Close", key="-CLOSE-", size=(12, 2))],
        ],
        expand_x=True,
        element_justification="c",
    )
    layout = [
        [sg.Text("Initial conditions:"), create_stretch()],
        [initial_conditions_table],
        [sg.Text("Coefficients:"), create_stretch()],
        [coefficient_table],
        [sg.Text("Social contact matrix:"), create_stretch()],
        [contact_table],
    ]
    main_frame = sg.Column(
        layout,
        element_justification="c",
        expand_x=True,
        expand_y=True,
    )

    vac_eff_text = create_col_for_row(sg.Text(text="Vaccination eff", size=(15, 1)))
    vac_eff_value = create_col_for_row(
        sg.InputText(
            f"{vac_parameters['eff']}",
            size=(20, 1),
            justification="right",
            key="vaccination_eff",
            disabled=not with_vac,
        )
    )
    vac_eff_row = create_row(vac_eff_text, create_stretch(), vac_eff_value, True)
    vac_layout = [[sg.Text("Vaccination parameters: ")], [vac_eff_row]]
    for i in range(1, 9):
        rate = vac_parameters[f"age_grp_{i}"][0]
        start = vac_parameters[f"age_grp_{i}"][1]
        end = vac_parameters[f"age_grp_{i}"][2]
        vac_rate_text = create_col_for_row(
            sg.Text(text="Vaccination rate", size=(15, 1))
        )
        vac_rate_value = create_col_for_row(
            sg.InputText(
                f"{rate}",
                size=(20, 1),
                justification="right",
                key=f"vaccination_rate_{i}",
                disabled=not with_vac,
            )
        )
        vac_rate_row = create_row(vac_rate_text, create_stretch(), vac_rate_value, True)
        vac_start_text = create_col_for_row(
            sg.Text(text="Vaccination start", size=(15, 1))
        )
        vac_start_value = create_col_for_row(
            sg.InputText(
                f"{start}",
                size=(20, 1),
                justification="right",
                key=f"vaccination_start_{i}",
                disabled=not with_vac,
            )
        )
        vac_start_row = create_row(
            vac_start_text, create_stretch(), vac_start_value, True
        )
        vac_end_text = create_col_for_row(sg.Text(text="Vaccination end", size=(15, 1)))
        vac_end_value = create_col_for_row(
            sg.InputText(
                f"{end}",
                size=(20, 1),
                justification="right",
                key=f"vaccination_end_{i}",
                disabled=not with_vac,
            )
        )
        vac_end_row = create_row(vac_end_text, create_stretch(), vac_end_value, True)

        vac_group_text = sg.Text(text=f"Age group {i}", size=(15, 1))
        vac_layout.append([vac_group_text])
        vac_layout.append([vac_rate_row])
        vac_layout.append([vac_start_row])
        vac_layout.append([vac_end_row])
    vac_layout = sg.Column(
        vac_layout, element_justification="c", expand_x=True, expand_y=True
    )
    return create_layout(param_buttons, main_frame, vac_layout)


def layout_stat(stats):
    if isinstance(stats, np.ndarray):
        stats = stats.tolist()

    stat_table = sg.Table(
        stats,
        headings=[
            "Age group",
            "Rₙ₀",
            "Maximum number of infectious asymptomatic people",
            "Maximum number of infectious symptomatic people",
            "Total number of deaths",
        ],
        expand_x=True,
        expand_y=True,
        auto_size_columns=False,
        col_widths=[8, 5, 35, 35, 20],
        hide_vertical_scroll=True,
        justification="c",
        num_rows=len(stats),
        font=(r"Helvetica 12"),
        key="-STATTAB-",
    )
    layout = [
        [stat_table],
    ]
    return create_layout(layout)
