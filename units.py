import os
import psutil
import platform
from datetime import datetime
import multiprocessing


class KpiUnits(object):
    def __init__(self):
        pass

    def SystemDetail(self):
        uname = platform.uname()
        system = uname.system
        node_name = uname.node
        release = uname.release
        version = uname.version
        machine = uname.machine
        processor = uname.processor
        boot_time = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time)
        last_boot = {'year':bt.year, 'month':bt.month, 'day':bt.day,'hour':bt.hour, 'minute':bt.minute, 'second':bt.second}
        logged_in = psutil.users()
        return {'system': system, 'node_name': node_name, 'release': release, 'version': version, 'machine': machine, 'processor': processor, 'lastboot': last_boot, 'users': logged_in}


    def TEMP(self):
            #temp = psutil.sensors_temperatures()
            #core0t = psutil.sensors_temperatures()['coretemp'][0][1]
            #core1t = psutil.sensors_temperatures()['coretemp'][1][1]
            #return [core0t, core1t]
            pass

    def PROCESS(self):
        # the list the contain all process dictionaries
        processes = []
        for process in psutil.process_iter():
            # get all process info in one shot
            with process.oneshot():
                # get the process id
                pid = process.pid
                if pid == 0:
                    # System Idle Process for Windows NT, useless to see anyways
                    continue
                    # get the name of the file executed
                name = process.name()
                # get the time the process was spawned
                try:
                    create_time = datetime.fromtimestamp(process.create_time())
                except OSError:
                    # system processes, using boot time instead
                    create_time = datetime.fromtimestamp(psutil.boot_time())
                try:
                    # get the number of CPU cores that can execute this process
                    cores = len(process.cpu_affinity())
                except psutil.AccessDenied:
                    cores = 0
                    # get the CPU usage percentage
                cpu_usage = process.cpu_percent()
                # get the status of the process (running, idle, etc.)
                status = process.status()
                try:
                    # get the process priority (a lower value means a more prioritized process)
                    nice = int(process.nice())
                except psutil.AccessDenied:
                    nice = 0
                try:
                    # get the memory usage in bytes
                    memory_usage = process.memory_full_info().uss
                except psutil.AccessDenied:
                    memory_usage = 0
                    # total process read and written bytes
                #io_counters = process.io_counters()
                io_counters = 'NA'
                #read_bytes = io_counters.read_bytes
                read_bytes = 'NA'
                #write_bytes = io_counters.write_bytes
                write_bytes = 'NA'
                # get the number of total threads spawned by this process
                n_threads = process.num_threads()
                # get the username of user spawned the process
                try:
                    username = process.username()
                except psutil.AccessDenied:
                    username = "N/A"
                processes.append({
                    'pid': pid, 'name': name, 'create_time': create_time,
                    'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
                    'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,'n_threads': n_threads, 'username': username,})
            return processes




class SystemUnits(object):
    def __init__(self):
        pass

    def CPU(self):
        # CPU usage
        #print("CPU Usage Per Core:")
        #for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        #    print(f"Core {i}: {percentage}%")
        #    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        #core_count = psutil.cpu_count(logical=False)
        #thread_count = psutil.cpu_count(logical=True)
        #cpufreq = {'capacity': psutil.cpu_freq().max, 'current':psutil.cpu_freq().current, 'min': psutil.cpu_freq().min}
        #usage = psutil.cpu_times_percent()
        #current = psutil.cpu_percent()/multiprocessing.cpu_count()
        #print('current cpu', current)
        return psutil.cpu_percent()
        #return dict({'cores': core_count, 'threads': thread_count, 'cpufreq': cpufreq, 'current': current, 'usage': {'user': usage.user, 'nice':usage.nice, 'system':usage.system, 'idle':usage.idle,'iowait':usage.iowait, 'irq':usage.irq, 'softirq': usage.softirq, 'steal': usage.steal, 'guest': usage.guest, 'guestnice': usage.guest_nice }})

    def LOAD(self):
        return psutil.getloadavg()[2]

    def RAM(self):
        #mem = psutil.virtual_memory()
        #swap = psutil.swap_memory()
        #return {'ram_total': mem.total, 'ram_available': mem.available, 'ram_used': mem.used , 'ram_percent': mem.percent, 'swap_total': swap.total, 'swap_free': swap.free, 'swap_used': swap.used , 'swap_percent': swap.percent}
        return psutil.virtual_memory()[2]

    def DISK(self):
        disk = {}
        count = 0
        partitions = psutil.disk_partitions()
        for partition in partitions:
            disk['device' + str(count)] = partition.device
            disk['mount_point'] = partition.mountpoint
            disk['file_system_type'] = partition.fstype
            count =+1
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk['total'] = partition_usage.total
                disk['used'] = partition_usage.used
                disk['free'] = partition_usage.free
                disk['percentage'] = partition_usage.percent
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
        disk_io = psutil.disk_io_counters()
        disk['total_read_io'] = disk_io.read_bytes
        disk['total_write_io'] = disk_io.write_bytes
        return disk

    def GPU(self):
        pass

    def BLUETOOTH(self):
        pass

    def NETWORK(self):
        net_io = psutil.net_io_counters()
        return net_io


#statistics = get_statistics()



