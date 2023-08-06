#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:52:33 2020

@author: ananya
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
from pudb import set_trace as bp  # noqa

import radiocc


def PLOT_Dop1(distance, Doppler, Doppler_debias, Doppler_biasfit, ET, PLOT_DIR, N_data):
    if radiocc.gui is not None:
        figure = radiocc.gui.figure
        figure.clear()
    else:
        figure = plt.figure(6)
        plt.ion()
        plt.show()

    axis_left = figure.add_subplot(121)
    axis_right = figure.add_subplot(122)
    figure.suptitle("Radio Occultation")
    figure.text(0.5, 0.04, "Doppler Frequency Residuals (Hz)", va="center", ha="center")
    figure.text(
        0.04, 0.5, "Altitude (km)", va="center", ha="center", rotation="vertical"
    )

    Doppler = np.array(Doppler)
    Doppler_debias = np.array(Doppler_debias)
    cond_dop = Doppler < 1
    cond_deb = Doppler_debias < 1

    axis_left.plot(
        Doppler, distance / 1000, ":", color="black", label="Raw L2 Data"
    )  # (1+880./749.)
    axis_left.plot(
        Doppler_debias,
        distance / 1000,
        ":",
        color="blue",
        label="Debias Raw L2 Data",
    )  # (1+880./749.)

    # FIXME:
    # + MEX enables lines below but not MAVEN, do we keep that?
    # + same for comment below 'xlim'
    #
    # Doppler = Doppler[cond_dop]
    # Doppler_debias = Doppler_debias[cond_deb]

    min_x1 = (
        np.nanmedian(Doppler_debias)
        - sc.median_absolute_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    min_x2 = (
        np.nanmedian(Doppler)
        - sc.median_absolute_deviation(Doppler, nan_policy="omit") * 5
    )
    max_x1 = (
        np.nanmedian(Doppler_debias)
        + sc.median_absolute_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    max_x2 = (
        np.nanmedian(Doppler)
        + sc.median_absolute_deviation(Doppler, nan_policy="omit") * 5
    )
    min_x = min([min_x1, min_x2])
    max_x = max([max_x1, max_x2])

    axis_left.set_ylim(3400, 4000)
    axis_left.set_xlim(min_x, max_x)
    axis_left.grid(True)
    axis_left.legend()

    delET = []  # np.full(N_data, np.nan)
    for i in range(N_data):
        delET.append(ET[i] - ET[0])

    axis_right.clear()
    axis_right.plot(
        np.array(delET), Doppler, "-", color="black", label="Raw L2 Data"
    )  # (1+880./749.)
    # plt.plot(ET,Doppler_debias, color='blue', label = 'Debias Raw L2 Data')#(1+880./749.)
    # axis_right.plot(np.array(ET),
    #   Doppler_biasfit,  ":", color="red", label="Linear regression"
    # )  # (1+880./749.)

    min_x1 = (
        np.nanmedian(Doppler_debias)
        - sc.median_absolute_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    min_x2 = (
        np.nanmedian(Doppler)
        - sc.median_absolute_deviation(Doppler, nan_policy="omit") * 5
    )
    max_x1 = (
        np.nanmedian(Doppler_debias)
        + sc.median_absolute_deviation(Doppler_debias, nan_policy="omit") * 5
    )
    max_x2 = (
        np.nanmedian(Doppler)
        + sc.median_absolute_deviation(Doppler, nan_policy="omit") * 5
    )
    min_x = min([min_x1, min_x2])
    max_x = max([max_x1, max_x2])

    # axis_right.set_xlim(min_x, max_x)
    axis_right.set_xlim(0, 500)
    axis_right.set_ylim(-0.3, 0.3)
    axis_right.grid(True)
    axis_right.legend()

    figure.savefig(PLOT_DIR + "/" + "Doppler_1.svg", dpi=100)
    if radiocc.gui is not None:
        radiocc.gui.draw()
    else:
        plt.pause(1.0)
        input("Press [enter] to continue.")
        plt.close()

    # fig7 = plt.figure(7)
    # plt.ion()
    # plt.show()
    # plt.plot(delET, Doppler, ":", color="black", label="Raw L2 Data")  # (1+880./749.)
    # plt.plot(
    #     delET,
    #     np.array(Doppler_debias) * 100,
    #     ":",
    #     color="blue",
    #     label="Debias Raw L2 Data",
    # )  # (1+880./749.)

    # plt.ylabel("Doppler Frequency Residuals (Hz)")
    # plt.xlabel("Time (sec)")

    # # plt.xlim(0, 6000)
    # plt.ylim(-10, 10)
    # # plt.xlim(-0.2,0.2)
    # plt.grid(True)
    # plt.legend()
    # fig7.set_size_inches(6, 10)  #
    # plt.savefig(PLOT_DIR + "/" + "Doppler_ET_before_Corr.png", dpi=600)
    # plt.pause(1.0)
    # input("Press [enter] to continue.")
    # plt.close()

    return
