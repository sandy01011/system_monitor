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

##
import docker
from running_app import get_running_apps
from contextlib import redirect_stdout

def get_docker_stats():
    docker_list = []
    #ps = subprocess.Popen(['docker ps'], stdout=subprocess.PIPE)
    client = docker.from_env()
    cont_all = client.containers.list(all)    #returns the list of all the containes
    for index, cont in enumerate(cont_all):
        docker_list.append((index+1, cont.name, cont.short_id, cont.status))
    docker_dict = {tup[0]: tup[1:] for tup in docker_list}
    return docker_list, cont_all

docker_stats, all_conts  = get_docker_stats()

def get_services():
    for cont in all_conts:
        if re.search(r'SMREVAMP_7.8.*', cont.name):
            tomcat_status = cont.exec_run("sh -c 'netstat -an | grep 10080'")
            tomcat_status = tomcat_status[1].decode('utf-8')
            print("Tomcat Status:", tomcat_status)
    #for c in docker_stats:
        #if re.search(r'SMRE*', c[1]):
            #print("This is SM container", c[1])
            #print("All conts", all_conts)
            #cmd = "docker exec -ti {} bash; ls".format(c[2])
            #tomcat_status = subprocess.Popen(cmd, shell=True)

#get_services()

def get_system_stats():
    statistics = {}
    #statistics['start_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    statistics['start_time'] =  datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    #statistics['hostname'] =  'bluemoon'
    statistics['hostname'] = KpiUnits.SystemDetail(object)['node_name']
    statistics['load'] = SystemUnits.LOAD(object)
    statistics['cpu'] = SystemUnits.CPU(object)
    #statistics['process'] = KpiUnits.PROCESS(object)
    statistics['process'] = json.dumps(get_running_apps())
    statistics['memory'] = SystemUnits.RAM(object)
    statistics['disk'] = SystemUnits.DISK(object)
    #statistics['cpu0temp'] = KpiUnits.TEMP(object)[0]
    #statistics['cpu1temp'] = KpiUnits.TEMP(object)[1]
    #statistics['network'] = SystemUnits.NETWORK(object)
    #statistics['end_time'] = {'year':datetime.now().year,'month':datetime.now().month,'day':datetime.now().day,'hour':datetime.now().hour,'minute':datetime.now().minute,'seconds':datetime.now().second, 'microsecond':datetime.now().microsecond}
    statistics['end_time'] =  datetime.now().strftime("%d/%m/%y-%H:%M:%S")
    #print('stats collected')
    #print('stats collected')
    #application = {}
    docker = docker_stats
    #docker = {}
    services = {}
    return {statistics['hostname']:{'os':statistics, 'application':{'docker':docker, 'services':services}}}
    #return {'os':statistics, 'application':{'docker':docker, 'services':services}}
    #return statistics
#stats_df = pd.DataFrame(get_system_stats(), columns=['start_time','load', 'cpu', 'memory', 'cpu0temp', 'cpu1temp'])
#stats_df.reset_index(inplace=True)
#data_dict = stats_df.to_dict('list')
#sys_stats = {'monitor': { 'type': 'sysmon', 'stats': get_system_stats()}}
#sys_stats = {'index':datetime.now(), 'statsdf':data_dict}
#sys_stats = {'index':'bluemoon', 'statsdf':data_dict}
#sys_stats = {'index':'bluemoon', 'statsdf':get_system_stats()}
sys_stats = get_system_stats()
print(sys_stats)
#LoadMetaData.load_bot_metadata_to_db(statistics['prime'])
load_monitor_data('collection',sys_stats)
path = '/home/sandeep/docker_volumes/rachit/nodemonDEV/'
filename = path + KpiUnits.SystemDetail(object)['node_name'] + '-' + datetime.now().strftime("%d_%m_%y-%H_%M_%S") + '.json'
with open(filename, 'a') as file:
    #print(sys_stats)
    data = sys_stats
    json.dump(data, file, default=str)
    file.close()

#print(statistics)
