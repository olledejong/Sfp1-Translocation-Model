import matplotlib.pyplot as plt
import numpy as np


def plot_abundances(tspan, y1, y2):
    fig, ax1 = plt.subplots()
    fig.suptitle("Cytoplasmic and nuclear protein abundances over time")
    ax1.set_xlabel('Time')
    ax1.grid(False)
    ax1.set_ylabel("Cytoplasmic protein abundance", color='orange')
    ax1.plot(tspan, y1, color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')
    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.set_ylabel("Nuclear protein abundance", color='darkred')
    ax2.plot(tspan, y2, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')
    plt.show()


def plot_volume_ratio(t_range, nuc_vols, cell_vols):
    plt.plot(t_range, nuc_vols / (cell_vols - nuc_vols), color='red', lw=2)
    plt.title("Nuclear to cytoplasmic volume ratio")
    plt.xlabel("Time")
    plt.ylabel("Ratio")
    plt.show()


def plot_abundance_ratio(final_tspan, final_cyt_ab, final_nuc_ab):
    plt.plot(final_tspan, final_cyt_ab / final_nuc_ab, color='red', lw=2)
    plt.title("Nuclear to cytoplasmic abundance ratio")
    plt.xlabel("Time")
    plt.ylabel("Ratio")
    plt.show()


def plot_concentration_ratio(final_tspan, final_cyt_ab, final_nuc_ab, cv_func, nv_func, num_nans):
    # get cell / nuc volumes for all timepoints
    cell_vols = [cv_func(t).flatten()[0] for t in final_tspan][:-num_nans]
    nuc_vols = [nv_func(t).flatten()[0] for t in final_tspan][:-num_nans]
    cyt_vols = [i - j for i, j in zip(cell_vols, nuc_vols)]

    # with the abundances, the event is distinctly happening over one time-step, this is not the case for the volumes.
    # this is because the volumes are first manipulated to represent nuclear division at one time-step, but after that
    # they are interpolated using the interp1d method. This causes a more transient simulation of that division.
    # therefore we need to slightly alter these to prevent plotting artifacts.
    nuc_vols[181:184] = [nuc_vols[180]] * len(nuc_vols[181:184])  # TODO make this dynamic (non-hardcoded indexes)

    # calculate the concentrations
    c_con = [i / j for i, j in zip(final_cyt_ab.tolist(), cyt_vols)]
    n_con = [i / j for i, j in zip(final_nuc_ab.tolist(), nuc_vols)]

    con_ratio = [i / j for i, j in zip(n_con, c_con)]

    plt.plot(final_tspan[:-num_nans], c_con, c='red', lw=2)
    plt.title("Cytoplasmic protein concentration")
    plt.xlabel("Time")
    plt.ylabel("Concentration")
    plt.show()

    plt.plot(final_tspan[:-num_nans], n_con, c='red', lw=2)
    plt.title("Nuclear protein concentration")
    plt.xlabel("Time")
    plt.ylabel("Concentration")
    plt.show()

    plt.plot(final_tspan[:-num_nans], con_ratio, c='red', lw=2)
    plt.title("Nuclear to cytoplasmic protein concentration ratio")
    plt.xlabel("Time")
    plt.ylabel("Ratio")
    plt.show()


def plot_multiple_cycles(cyt_ab_cycles, nuc_ab_cycles):
    fig, ax1 = plt.subplots()
    fig.suptitle("Cytoplasmic and nuclear protein abundances over time")
    ax1.set_xlabel('Time')
    ax1.grid(False)
    ax1.set_ylabel("Cytoplasmic protein abundance", color='orange')
    ax1.plot(cyt_ab_cycles, color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')
    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.set_ylabel("Nuclear protein abundance", color='darkred')
    ax2.plot(nuc_ab_cycles, color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')
    plt.show()
