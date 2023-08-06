#!/usr/bin/env python3

"""
radiocc
"""

import logging
import os
import string
from pathlib import Path
from typing import Optional

from radiocc import config, download_data, interface, process_descriptor
from radiocc.core import run

from .model import Bands, Layers

__all__ = [
    "Bands",
    "Layers",
    "run",
]

# Project variables.
NAME = "radiocc"
VERSION = "0.6.9"

# Logging settings.
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(name)s[%(levelname)s]: %(message)s"
LOG_DATEFMT = "%m/%d/%Y %I:%M:%S %p"

# Runtime variables.
SRC_PATH = Path(os.path.realpath(__file__)).parent
ASSETS_PATH = SRC_PATH / "assets"
CFG_PATH = Path(f"{NAME}.yaml")
LOG_PATH = Path(f"{NAME}.log")
INFORMATION_PATH = ASSETS_PATH / "information"
DESCRIPTOR_FILENAME = "descriptor.yaml"

# Start logging.
logging.basicConfig(
    filename=LOG_PATH,
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATEFMT,
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
LOGGER = logging.getLogger(NAME)
LOGGER.info("Logging enabled.")

# Configurable parameters definition.
cfg = config.Cfg()
gui: Optional[interface.Interface] = None

# General Constants.
SPICE_MAVEN_DIRECTORY = Path("spice-maven/mk")
TEMPORARY_DOWNLOAD_DIRECTORY = Path("temporary-download-location")
MAVEN_DIRNAME_TEMPLATE = string.Template("maven $DATE")
DATE_FMT_FOLDER = "YYYY-MMM-DD HH:mm:ss"
