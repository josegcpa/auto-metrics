"""
Contains generic logging utilities.
"""

import logging

logger = logging.getLogger("Auto-METRICS")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(name)s %(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)
