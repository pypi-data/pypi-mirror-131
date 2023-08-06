__version__ = "1.0"
__author__ = "Xie Hai"

import sys
import logging

if sys.version_info < (3, 6):
    print(f"spoceatmos {__version__} requires Python 3.6+ and 64 bit OS")
    sys.exit(1)

del sys

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] SPOCEATMOS >>> %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# ---------------------------------------------------------
# GOES SOLAR ULTRAVIOLET IMAGER (SUVI)
# 太阳紫外线成像卫星
# ---------------------------------------------------------
# National Oceanic and Atmospheric Administration(NOAA)
# 美国国家海洋和大气管理局
# SPACE WEATHER PREDICTION CENTER
# 太空气象预报中心
# GOES SOLAR ULTRAVIOLET IMAGER (SUVI)
# ---------------------------------------------------------
from spoceatmos.noaa.swpc.suvi import suvi
