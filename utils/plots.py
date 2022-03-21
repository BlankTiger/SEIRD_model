import matplotlib.pyplot as plt

colors = [
    "#008fd5",
    "#fc4f30",
    "#e5ae38",
    "#0d904f",
    "#9c9c9c",
    "#800f7c",
    "#000000",
    "#00e10f",
]


def plot_SEIRD(t, y, screen_size):
    dpi = 100
    fig_width = 13
    fig_height = 8

    if screen_size.width < 1920:
        fig_width = fig_width * screen_size.width / 1920
        fig_height = fig_height * screen_size.height / 1080

    plt.style.use("fivethirtyeight")
    plt.rcParams.update({"font.size": 10})
    fig, ax = plt.subplots(
        3,
        2,
        sharex=True,
        gridspec_kw={
            "height_ratios": [1, 1, 1],
            "hspace": 0.15,
            "left": 0.088,
            "right": 0.967,
            "top": 0.967,
            "bottom": 0.088,
        },
    )
    plt.gcf()
    fig.set_dpi(dpi)
    fig.set_figwidth(fig_width)
    fig.set_figheight(fig_height)
    labels = [
        [f"$S_{i}$" for i in range(1, 9)],
        [f"$E_{i}$" for i in range(1, 9)],
        [f"$I_{{s,{i}}}$" for i in range(1, 9)],
        [f"$I_{{a,{i}}}$" for i in range(1, 9)],
        [f"$R_{i}$" for i in range(1, 9)],
        [f"$D_{i}$" for i in range(1, 9)],
    ]
    for i in range(8):
        ax[0, 0].plot(t, y[0][:, i], color=colors[i], label=labels[0][i], lw=1)
        ax[0, 1].plot(t, y[1][:, i], color=colors[i], label=labels[1][i], lw=1)
        ax[1, 0].plot(t, y[2][:, i], color=colors[i], label=labels[2][i], lw=1)
        ax[1, 1].plot(t, y[3][:, i], color=colors[i], label=labels[3][i], lw=1)
        ax[2, 0].plot(t, y[4][:, i], color=colors[i], label=labels[4][i], lw=1)
        ax[2, 1].plot(t, y[5][:, i], color=colors[i], label=labels[5][i], lw=1)

    for i in range(3):
        for j in range(2):
            legend = ax[i, j].legend(
                fontsize="small",
                ncol=2,
                fancybox=True,
                shadow=True,
                borderpad=0.5,
                frameon=True,
            )
            for line in legend.get_lines():
                line.set_linewidth(3)
            ax[i, j].ticklabel_format(axis="y", useOffset=False, style="plain")
            ax[i, j].set_xlabel("Time [days]")
            ax[i, j].set_ylabel("Population")

    plt.text(
        0.1,
        0.97,
        "© M. Urban, J. Jodłowska, J. Balbus, K. Kubica",
        fontsize=10,
        transform=plt.gcf().transFigure,
    )
    return fig
