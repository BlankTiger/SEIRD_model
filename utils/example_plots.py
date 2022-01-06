import matplotlib.pyplot as plt
import numpy as np


def cmp_age_group_sol(solutions):
    # compare each age group's solutions to 6 diff eqs
    fig, axs = plt.subplots(
        3,
        2,
        sharex=True,
        gridspec_kw={"height_ratios": [1.5, 1.5, 1.5], "hspace": 0.15},
    )
    plt.gcf()
    plt.style.use("fivethirtyeight")
    plt.rcParams.update({"font.size": 9})
    labels = [
        [f"S$_{i}$" for i in range(1, 9)],
        [f"E$_{i}$" for i in range(1, 9)],
        [r"I$_{s," + str(i) + r"}$" for i in range(1, 9)],
        [r"I$_{a," + str(i) + r"}$" for i in range(1, 9)],
        [f"R$_{i}$" for i in range(1, 9)],
        [f"D$_{i}$" for i in range(1, 9)],
    ]
    for i in range(8):
        axs[0, 0].plot(
            solutions[0], solutions[1][:, i], label=labels[0][i], lw=1
        )
        axs[0, 1].plot(
            solutions[0], solutions[2][:, i], label=labels[1][i], lw=1
        )
        axs[1, 0].plot(
            solutions[0], solutions[3][:, i], label=labels[2][i], lw=1
        )
        axs[1, 1].plot(
            solutions[0], solutions[4][:, i], label=labels[3][i], lw=1
        )
        axs[2, 0].plot(
            solutions[0], solutions[5][:, i], label=labels[4][i], lw=1
        )
        axs[2, 1].plot(
            solutions[0], solutions[6][:, i], label=labels[5][i], lw=1
        )
    for i in range(3):
        for j in range(2):
            axs[i, j].legend(
                fontsize="small",
                ncol=2,
                fancybox=True,
                shadow=True,
                borderpad=0.5,
                frameon=True,
            )
            axs[i, j].ticklabel_format(
                axis="y", useOffset=False, style="plain"
            )
            axs[i, j].set_xlabel("Time [days]")
            axs[i, j].set_ylabel("Population")
    plt.xticks(
        np.arange(
            min(solutions[0]),
            55,
            5,
        )
    )
    plt.show()


def all_sol_in_grid(solutions):
    # One way to plot solutions in a 8x6 grid
    fig, axs = plt.subplots(8, 6, sharex=True)
    plt.gcf()
    plt.style.use("fivethirtyeight")
    plt.rcParams.update({"font.size": 9})
    axs.flatten()
    fig.set_size_inches(19, 19)
    plt.autoscale()
    for i in range(8):
        for j in range(6):
            axs[i, j].plot(solutions[0], solutions[j + 1][:, i])
            axs[i, j].ticklabel_format(
                axis="y", useOffset=False, style="plain"
            )
    plt.tight_layout()
    plt.savefig("sweden_SEIRD.pdf", bbox_inches="tight")
