import matplotlib.pyplot as plt
import numpy as np


def plot_SEIRD(t, y, coeff, contact):
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
    fig.set_figwidth(13)
    fig.set_figheight(8)
    labels = [
        [f"S$_{i}$" for i in range(1, 9)],
        [f"E$_{i}$" for i in range(1, 9)],
        [r"I$_{s," + str(i) + r"}$" for i in range(1, 9)],
        [r"I$_{a," + str(i) + r"}$" for i in range(1, 9)],
        [f"R$_{i}$" for i in range(1, 9)],
        [f"D$_{i}$" for i in range(1, 9)],
    ]
    for i in range(8):
        ax[0, 0].plot(t, y[0][:, i], label=labels[0][i], lw=1)
        ax[0, 1].plot(t, y[1][:, i], label=labels[1][i], lw=1)
        ax[1, 0].plot(t, y[2][:, i], label=labels[2][i], lw=1)
        ax[1, 1].plot(t, y[3][:, i], label=labels[3][i], lw=1)
        ax[2, 0].plot(t, y[4][:, i], label=labels[4][i], lw=1)
        ax[2, 1].plot(t, y[5][:, i], label=labels[5][i], lw=1)

    for i in range(3):
        for j in range(2):
            ax[i, j].legend(
                fontsize="small",
                ncol=2,
                fancybox=True,
                shadow=True,
                borderpad=0.5,
                frameon=True,
            )
            ax[i, j].ticklabel_format(axis="y", useOffset=False, style="plain")
            ax[i, j].set_xlabel("Time [days]")
            ax[i, j].set_ylabel("Population")
    return fig
