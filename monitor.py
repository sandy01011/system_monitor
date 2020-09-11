import datetime
import os
import subprocess
import re
import shutil
#from dbl import LoadMetaData, load_bot_metadata
from units import *
from dbm import load_monitor_data


def get_system_stats():
    statistics = {}
    statistics['start_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    statistics['prime'] = KpiUnits.SystemDetail(object)
    statistics['cpu'] = SystemUnits.CPU(object)
    statistics['process'] = KpiUnits.PROCESS(object)
    statistics['memory'] = SystemUnits.RAM(object)
    statistics['disk'] = SystemUnits.DISK(object)
    statistics['temprature'] = KpiUnits.TEMP(object)
    statistics['network'] = SystemUnits.NETWORK(object)
    statistics['end_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    print('stats collected')
    return statistics

sys_stats = {'monitor': { 'type': 'sysmon', 'stats': get_system_stats()}}

#LoadMetaData.load_bot_metadata_to_db(statistics['prime'])
load_monitor_data(sys_stats)
#print(statistics)
