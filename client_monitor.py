import datetime
import os
import subprocess
import re
import shutil
import pandas as pd
#from dbl import LoadMetaData, load_bot_metadata
from units import *
import json
from dbm import load_monitor_data

# docker monitor
import docker
from running_app import get_running_apps
from contextlib import redirect_stdout

def get_docker_stats():
    docker_list = []
    try:
        client = docker.from_env()
        cont_all = client.containers.list(all)    #returns the list of all the containes
        for index, cont in enumerate(cont_all):
            docker_list.append((index+1, cont.name, cont.short_id, cont.status))
        docker_dict = {tup[0]: tup[1:] for tup in docker_list}
        return docker_list, cont_all
    except Exception as e:
        print('error occurd while collecting docker information',e)
        docker_list = ['NA']
        cont_all = 0
        return docker_list, cont_all


docker_stats, all_conts  = get_docker_stats()

# service monitor
def get_services():
    pass

# system monitor
def get_system_stats():
    statistics = {}
    statistics['start_time'] =  datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    statistics['hostname'] = KpiUnits.SystemDetail(object)['node_name']
    statistics['load'] = SystemUnits.LOAD(object)
    statistics['cpu'] = SystemUnits.CPU(object)
    statistics['process'] = json.dumps(get_running_apps())
    statistics['memory'] = SystemUnits.RAM(object)
    statistics['disk'] = SystemUnits.DISK(object)
    statistics['end_time'] =  datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    docker = docker_stats
    services = {}
    return {statistics['hostname']:{'os':statistics, 'application':{'docker':docker, 'services':services}}}
sys_stats = get_system_stats()
print(sys_stats)
# write monitor data to mongodb
load_monitor_data('collection',sys_stats)
# write monitor data to json file
json_path = './monitor_data/'
json_file = json_path + KpiUnits.SystemDetail(object)['node_name'] + '-' + datetime.now().strftime("%d_%m_%y-%H_%M_%S") + '.json'
with open(json_file, 'a') as file:
    data = sys_stats
    json.dump(data, file, default=str)
    file.close()

#print(statistics)
