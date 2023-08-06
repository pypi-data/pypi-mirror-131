#!/usr/bin/env python3

"""
Radio occultation.
"""

from pathlib import Path

from pudb import set_trace as bp  # noqa: F401

import radiocc
from radiocc import constants, export, old, process_parser, reconstruct
from radiocc.model import Bands, Layers, ResultsFolders, Scenario
from radiocc.old import R17_Plot_profiles

BANDS = (Bands.X,)
LAYERS = (Layers.Iono, Layers.Atmo)


def run_with_gui() -> None:
    """Run radiocc with graphical interface."""
    radiocc.gui = radiocc.interface.Interface()

    radiocc.gui.set_altitude(constants.Threshold_Cor)


def run() -> None:
    """Run radiocc."""
    if radiocc.cfg.graphical_interface and radiocc.gui is None:
        run_with_gui()

    TO_PROCESS_DIRS = radiocc.utils.directories(
        radiocc.cfg.to_process,
        EXCLUDES=[
            ".*",
            "spice-maven",
            "temporary-download-location",
            "spice-maven-alternative",
        ],
    )
    for INDEX_PROCESS, PROCESS_PATH in enumerate(TO_PROCESS_DIRS):
        print(f"Reading {PROCESS_PATH.name}..")

        for BAND in BANDS:
            print(f"  Band: {BAND.name}")

            for LAYER in LAYERS:
                print(f"    Layer: {LAYER.name}")

                SCENARIO = Scenario(PROCESS_PATH, BAND, LAYER, INDEX_PROCESS)

                run_scenario(SCENARIO)

            band_export(SCENARIO)

    if radiocc.gui is not None:
        radiocc.gui.label_data.set_label("FINISHED!")
        radiocc.gui.mainloop()


def run_scenario(SCENARIO: Scenario) -> None:
    """Run a scenario."""
    if radiocc.gui is not None:
        radiocc.gui.label_data.set_label(
            f'PROCESSING "{SCENARIO.TO_PROCESS.name}" '
            f"Bande:{SCENARIO.BAND.value} Layer:{SCENARIO.LAYER.value}..."
        )
        radiocc.gui.draw()

    process_parser.prepare_directories(SCENARIO)
    FOLDER_TYPE = process_parser.detect_folder_type(SCENARIO.TO_PROCESS)

    if FOLDER_TYPE is None:
        return None

    process_parser.load_spice_kernels(SCENARIO, FOLDER_TYPE)
    L2_DATA = process_parser.read_L2_data(SCENARIO, FOLDER_TYPE)

    if L2_DATA is None:
        return None

    EXPORT = reconstruct.run(SCENARIO, L2_DATA)

    export.run(SCENARIO, L2_DATA, EXPORT)


def band_export(SCENARIO: Scenario) -> None:
    """Finish the plots for the layers of a scenario."""
    # Interface with old code.
    RESULTS = SCENARIO.results(radiocc.cfg.results)
    i_Profile = SCENARIO.INDEX_PROCESS
    DATA_PRO = str(SCENARIO.TO_PROCESS.parent)
    DATA_ID = str(SCENARIO.TO_PROCESS.resolve())
    CODE_DIR = str(Path(old.__file__).parent.resolve())
    DATA_DIR = str(SCENARIO.TO_PROCESS.parent.parent.resolve())
    PLOT_DIR = str((RESULTS / ResultsFolders.PLOTS.name).resolve())
    DATA_FINAL_DIR = str((RESULTS / ResultsFolders.DATA.name).resolve())

    R17_Plot_profiles.PLOT2(  # type: ignore [no-untyped-call]
        DATA_ID,
        i_Profile,
        DATA_PRO,
        CODE_DIR,
        SCENARIO.BAND.name,
        DATA_DIR,
        constants.Threshold_Cor,
        constants.Threshold_Surface,
        DATA_FINAL_DIR,
        PLOT_DIR,
        constants.Threshold_int,
    )
