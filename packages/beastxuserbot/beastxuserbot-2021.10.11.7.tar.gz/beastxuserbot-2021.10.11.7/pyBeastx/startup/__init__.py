# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyBeastx/blob/main/LICENSE>.

import os
import time
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger

from telethon import __version__

from ..version import __version__ as __beastx__
from ..version import beastx_version

if os.path.exists("beast.log"):
    os.remove("beast.log")

LOGS = getLogger("pyBeastLogs")
TeleLogger = getLogger("Telethon")
TeleLogger.setLevel(WARNING)

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("beast.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


LOGS.info(f"py-Beast Version - {__beastx__}")
LOGS.info(f"Telethon Version - {__version__}")
LOGS.info(f"Beast Version - {beastx_version}")
