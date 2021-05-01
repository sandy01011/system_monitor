import datetime
import os
import subprocess
import re
import shutil
import pandas as pd
#from dbl import LoadMetaData, load_bot_metadata
from units import *
from dbm import load_monitor_data


def get_system_stats():
    statistics = {}
    #statistics['start_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    statistics['start_time'] =  datetime.now()
    #statistics['hostname'] =  'bluemoon'
    statistics['hostname'] = KpiUnits.SystemDetail(object)['node_name']
    statistics['load'] = SystemUnits.LOAD(object)
    statistics['cpu'] = SystemUnits.CPU(object)
    #statistics['process'] = KpiUnits.PROCESS(object)
    statistics['memory'] = SystemUnits.RAM(object)
    #statistics['disk'] = SystemUnits.DISK(object)
    statistics['cpu0temp'] = KpiUnits.TEMP(object)[0]
    statistics['cpu1temp'] = KpiUnits.TEMP(object)[1]
    #statistics['network'] = SystemUnits.NETWORK(object)
    statistics['end_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    statistics['end_time'] =  datetime.now()
    print('stats collected')
    return statistics
#stats_df = pd.DataFrame(get_system_stats(), columns=['start_time','load', 'cpu', 'memory', 'cpu0temp', 'cpu1temp'])
#stats_df.reset_index(inplace=True)
#data_dict = stats_df.to_dict('list')
#sys_stats = {'monitor': { 'type': 'sysmon', 'stats': get_system_stats()}}
#sys_stats = {'index':datetime.now(), 'statsdf':data_dict}
#sys_stats = {'index':'bluemoon', 'statsdf':data_dict}
#sys_stats = {'index':'bluemoon', 'statsdf':get_system_stats()}
sys_stats = get_system_stats()
#print(sys_stats)
#LoadMetaData.load_bot_metadata_to_db(statistics['prime'])
load_monitor_data('collection',sys_stats)
#print(statistics)
