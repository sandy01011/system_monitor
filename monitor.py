import os
import subprocess
import re
import shutil
from units import *


def get_stats():
    statistics = {}
    statistics['prime'] = KpiUnits.SystemDetail(object)
    statistics['cpu'] = SystemUnits.CPU(object)
    statistics['process'] = KpiUnits.PROCESS(object)
    statistics['memory'] = SystemUnits.RAM(object)
    statistics['disk'] = SystemUnits.DISK(object)
    statistics['temprature'] = KpiUnits.TEMP(object)
    statistics['network'] = SystemUnits.NETWORK(object)
    return statistics

statistics = get_stats()

print(statistics)
