import PySimpleGUI as sg
from dataclasses import dataclass


sg.theme("DarkGrey5")


@dataclass
class ScreenSettings:
    text_size: tuple = (13, 1)
    input_text_size: tuple = (13, 1)
    vac_text_size: tuple = (15, 1)
    vac_input_text_size: tuple = (20, 1)
    button_size: tuple = (13, 2)
    stat_button_size: tuple = (12, 1)
    canvas_size: tuple = (1300, 800)
    toolbar_size: tuple = (1300, 0)
    col_width: int = 10
    row_height: int = 35
    disabled_bg: str = "#3e3e3e"
    font: tuple = (r"Helvetica", 12)
    vac_font: tuple = (r"Helvetica", 12)
    tab_font: tuple = (r"Helvetica", 12)
    stat_font: tuple = (r"Helvetica", 12)
    vac_scrollable: bool = False


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


def create_vac_row(elem_1, elem_2, row_key=""):
    return sg.Column(
        [[create_stretch(), elem_1, create_stretch(), elem_2, create_stretch()]],
        key=row_key,
        visible=True,
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


settings = ScreenSettings()


def layout(screen_size):
    global settings
    if screen_size.width < 1920:
        settings.canvas_size = (
            settings.canvas_size[0] * screen_size.width / 1920,
            settings.canvas_size[1] * screen_size.width / 1920,
        )
        settings.toolbar_size = (settings.canvas_size[0], 0)
        settings.row_height = 24
        settings.font = (r"Helvetica", 9)
        settings.tab_font = (r"Helvetica", 8)
        settings.vac_font = (r"Helvetica", 8)
        settings.stat_font = (r"Helvetica", 9)
        settings.vac_scrollable = True
        print(settings.canvas_size)

    duration_text = sg.Text("Duration in days:", size=settings.text_size, expand_x=True)
    duration_input = sg.InputText(
        "100",
        key="-DURATION-",
        size=settings.input_text_size,
        justification="right",
        expand_x=True,
    )
    duration_text_row = create_row(
        create_stretch(), duration_text, create_stretch(), True
    )
    duration_input_row = create_row(
        create_stretch(), duration_input, create_stretch(), True
    )

    param_row = create_row(
        create_stretch(),
        sg.Button(
            "Parameters", key="-PARAM-", size=settings.button_size, expand_x=True
        ),
        create_stretch(),
        True,
    )

    stat_row = create_row(
        create_stretch(),
        sg.Button("Statistics", key="-STAT-", size=settings.button_size, expand_x=True),
        create_stretch(),
        True,
    )

    draw_row = create_row(
        create_stretch(),
        sg.Button("Plot", key="-DRAW-", size=settings.button_size, expand_x=True),
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
                    size=settings.canvas_size,
                )
            ],
            [
                sg.Canvas(
                    key="-TOOLBAR-",
                    background_color="white",
                    size=settings.toolbar_size,
                    expand_x=True,
                    expand_y=False,
                )
            ],
        ],
        expand_y=True,
        expand_x=True,
    )
    return create_layout(column1, column2)


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


def layout_param(parameters=params, vac_parameters=vac_parameters, with_vac=False):
    vertical_scroll = True
    y0_sweden = parameters["-INITIALTAB-"].astype(str)
    sweden_coefficients = parameters["-PARAMTAB-"].astype(str)
    sweden_contact_matrix = parameters["-CONTACTTAB-"].astype(str)

    left_headings = np.array(
        [
            [
                "Sₙ(0)",
                "Eₙ(0)",
                "Iₐ,ₙ(0)",
                "Iₛ,ₙ(0)",
                "Rₙ(0)",
                "Dₙ(0)",
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

    initial_conditions_table = sg.Table(
        y0_sweden.tolist(),
        headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=settings.row_height,
        def_col_width=settings.col_width,
        auto_size_columns=False,
        key="-INITIALTAB-",
        num_rows=6,
        expand_x=True,
        font=settings.tab_font,
        enable_click_events=True,
    )

    coefficient_table = sg.Table(
        sweden_coefficients.tolist(),
        headings=["Parameter", "n=1", "n=2", "n=3", "n=4", "n=5", "n=6", "n=7", "n=8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=settings.row_height,
        def_col_width=settings.col_width,
        auto_size_columns=False,
        key="-PARAMTAB-",
        num_rows=7,
        expand_x=True,
        font=settings.tab_font,
        enable_click_events=True,
    )

    contact_table = sg.Table(
        sweden_contact_matrix.tolist(),
        headings=["n", "1", "2", "3", "4", "5", "6", "7", "8"],
        hide_vertical_scroll=vertical_scroll,
        row_height=settings.row_height,
        def_col_width=settings.col_width,
        auto_size_columns=False,
        key="-CONTACTTAB-",
        num_rows=8,
        expand_x=True,
        font=settings.tab_font,
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
            [sg.Button("Save", key="-SAVE-", size=settings.button_size)],
            [create_stretch()],
            [sg.Button("Save to file", key="-SAVEFILE-", size=settings.button_size)],
            [create_stretch()],
            [sg.Button("Load from file", key="-LOADFILE-", size=settings.button_size)],
            [create_stretch()],
            [sg.Button("Load default", key="-LOADDEFAULT-", size=settings.button_size)],
            [create_stretch()],
            [sg.Button("Close", key="-CLOSE-", size=settings.button_size)],
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

    vac_eff_text = create_col_for_row(
        sg.Text(
            text="Vaccination eff", size=settings.vac_text_size, font=settings.vac_font
        )
    )
    vac_eff_value = create_col_for_row(
        sg.InputText(
            f"{vac_parameters['eff']}",
            size=settings.vac_input_text_size,
            justification="right",
            key="vaccination_eff",
            disabled=not with_vac,
            font=settings.vac_font,
            disabled_readonly_background_color=settings.disabled_bg,
        )
    )
    vac_eff_row = create_row(vac_eff_text, create_stretch(), vac_eff_value, True)
    vac_layout = [[sg.Text("Vaccination parameters: ", font=settings.vac_font)]]
    vac_elems = [[vac_eff_row]]
    for i in range(1, 9):
        rate = vac_parameters[f"age_grp_{i}"][0]
        start = vac_parameters[f"age_grp_{i}"][1]
        end = vac_parameters[f"age_grp_{i}"][2]
        vac_rate_text = create_col_for_row(
            sg.Text(
                text="Vaccination rate",
                size=settings.vac_text_size,
                font=settings.vac_font,
            )
        )
        vac_rate_value = create_col_for_row(
            sg.InputText(
                f"{rate}",
                size=settings.vac_input_text_size,
                justification="right",
                key=f"vaccination_rate_{i}",
                disabled=not with_vac,
                font=settings.vac_font,
                disabled_readonly_background_color=settings.disabled_bg,
            )
        )
        vac_rate_row = create_row(vac_rate_text, create_stretch(), vac_rate_value, True)
        vac_start_text = create_col_for_row(
            sg.Text(
                text="Vaccination start",
                size=settings.vac_text_size,
                font=settings.vac_font,
            )
        )
        vac_start_value = create_col_for_row(
            sg.InputText(
                f"{start}",
                size=settings.vac_input_text_size,
                justification="right",
                key=f"vaccination_start_{i}",
                disabled=not with_vac,
                font=settings.vac_font,
                disabled_readonly_background_color=settings.disabled_bg,
            )
        )
        vac_start_row = create_row(
            vac_start_text, create_stretch(), vac_start_value, True
        )
        vac_end_text = create_col_for_row(
            sg.Text(
                text="Vaccination end",
                size=settings.vac_text_size,
                font=settings.vac_font,
            )
        )
        vac_end_value = create_col_for_row(
            sg.InputText(
                f"{end}",
                size=settings.vac_input_text_size,
                justification="right",
                key=f"vaccination_end_{i}",
                disabled=not with_vac,
                font=settings.vac_font,
                disabled_readonly_background_color=settings.disabled_bg,
            )
        )
        vac_end_row = create_row(vac_end_text, create_stretch(), vac_end_value, True)

        vac_group_text = sg.Text(
            text=f"Age group {i}", size=settings.vac_text_size, font=settings.vac_font
        )
        vac_elems.append([vac_group_text])
        vac_elems.append([vac_rate_row])
        vac_elems.append([vac_start_row])
        vac_elems.append([vac_end_row])
    vac_elems = sg.Column(
        vac_elems,
        element_justification="c",
        expand_x=True,
        expand_y=True,
        scrollable=settings.vac_scrollable,
        vertical_scroll_only=True,
    )
    vac_layout.append([vac_elems])
    vac_layout = sg.Column(
        vac_layout,
        element_justification="c",
        expand_x=True,
        expand_y=True,
    )
    return create_layout(param_buttons, main_frame, vac_layout)


def layout_stat(stats):
    if isinstance(stats, np.ndarray):
        stats = stats.tolist()

    headings = [
        " n ",
        "R_n0",
        "max(I_an)",
        "max(I_sn)",
        "D_n(t_max)",
    ]

    stat_table = sg.Table(
        stats,
        headings=headings,
        expand_x=True,
        expand_y=True,
        auto_size_columns=True,
        # col_widths=[5, 9, 9, 9, 9],
        hide_vertical_scroll=True,
        justification="c",
        num_rows=len(stats),
        font=settings.stat_font,
        key="-STATTAB-",
    )
    save_button = sg.Button(
        "Save statistics", key="-SAVESTATS-", size=settings.stat_button_size
    )
    save_row = create_row(create_stretch(), save_button, create_stretch(), True)
    layout = [[stat_table], [save_row]]
    return create_layout(layout)
