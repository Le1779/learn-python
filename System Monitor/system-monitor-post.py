import requests
import socket
from uuid import getnode as get_mac
from datetime import datetime
from threading import Timer
import time
import psutil
import json

device_name = '';
device_mac_address = '';
doc = {
    'cpu': {
        'core': 0,
        'threads': 0,
        'usage_rate': []
    },
    'memory': {
        'total': 0,
        'free': 0,
        'usage_rate': 0
    },
    'disk': [],
    'network':{
        'receive': 0,
        'send': 0,
        'usage': 0
    }
}

def get_device_name():
    global device_name
    device_name = socket.gethostname()
    print(device_name)

def get_device_mac_address():
    global device_mac_address
    device_mac_address = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    print(device_mac_address)

def get_device_id():
    post_data = {'name':device_name,'macAddress':device_mac_address}
    r = requests.post('http://dfo.dynacw.com:57555/Device/GetDeviceId', data = post_data)
    if r.status_code == requests.codes.ok:
        return r.json()['id']
    else:
        return 0

def get_cpu_info():
    cpu_core = psutil.cpu_count(logical=False);
    cpu_threads = psutil.cpu_count(logical=True);
    cpu_usage_rate = psutil.cpu_percent(interval=1, percpu=True)

    
    doc['cpu']['core'] = cpu_core;
    doc['cpu']['threads'] = cpu_threads;
    doc['cpu']['usage_rate'] = cpu_usage_rate;

def get_memory_info():
    memory_free = round(psutil.virtual_memory().free/(1024.0*1024.0*1024.0), 2);
    memory_total = round(psutil.virtual_memory().total/(1024.0*1024.0*1024.0), 2);
    memory_usage_rate = round((memory_total-memory_free)/memory_total, 2)*100;

    doc['memory']['total'] = memory_total;
    doc['memory']['free'] = memory_free;
    doc['memory']['usage_rate'] = memory_usage_rate;

def get_disk_info():
    doc['disk'] = []
    disk_info = psutil.disk_partitions();
    for i in disk_info:
        if(i.fstype == 'NTFS'):
            disk_usage = psutil.disk_usage(i.device);
            disk_total = round(disk_usage.total/(1024.0*1024.0*1024.0), 2);
            disk_used = round(disk_usage.used/(1024.0*1024.0*1024.0), 2);
            disk_free = round(disk_usage.free/(1024.0*1024.0*1024.0), 2);
            disk_usage_rate = round(disk_used/disk_total, 2)*100;

            diskInfo = {};
            diskInfo['name'] = i.device;
            diskInfo['total'] = disk_total;
            diskInfo['used'] = disk_used;
            diskInfo['free'] = disk_free;
            diskInfo['usage_rate'] = disk_usage_rate;
            doc['disk'].append(diskInfo);

def get_network_info():
    net = psutil.net_io_counters();
    bytes_receive = net.bytes_recv;
    bytes_sent = net.bytes_sent;
    bytes_all = bytes_receive + bytes_sent;

    time.sleep(1);
    net = psutil.net_io_counters();
    bytes_receive = net.bytes_recv - bytes_receive
    bytes_sent = net.bytes_sent - bytes_sent    
    bytes_usage = net.bytes_recv + net.bytes_sent - bytes_all

    doc['network']['receive'] = bytes_receive;
    doc['network']['send'] = bytes_sent;
    doc['network']['usage'] = bytes_usage;

def post_device_info(device_id):
    post_data = {'deviceId':device_id, 'cpu':json.dumps(doc['cpu']), 'memory':json.dumps(doc['memory']), 'disk':json.dumps(doc['disk']), 'network':json.dumps(doc['network'])}
    r = requests.post('http://dfo.dynacw.com:57555/DeviceInfo/InsertInfo', data = post_data)
    if r.status_code == requests.codes.ok:
        print('success')
    else:
        print('failure')

def showData():
    showCPUInfo(doc['cpu']['core'], doc['cpu']['threads'])
    for i in range(len(doc['cpu']['usage_rate'])):
        showCPUUsageRate(i, doc['cpu']['usage_rate'][i]);
    
    showMemoryInfo(doc['memory']['total'], doc['memory']['free'], doc['memory']['usage_rate']);

    for diskInfo in doc['disk']:
        showDiskInfo(diskInfo['name'], diskInfo['total'], diskInfo['used'], diskInfo['free'], diskInfo['usage_rate']);
    
    showNetword(doc['network']['receive'], doc['network']['send'], doc['network']['usage']);

def showCPUInfo(core, threads):
    print ('CPU {0}核{1}線程'.format(core, threads));

def showCPUUsageRate(threads, usage_rate):
    print ('CPU {0}線程使用率: {1}%'.format(threads, usage_rate));

def showMemoryInfo(total, free, usage_rate):
    print ('記憶體 總共:{0}GB 剩餘:{1}GB 使用率:{2}%'.format(total, free, usage_rate));

def showDiskInfo(name, total, used, free, usage_rate):
    print ('硬碟{0} 總共:{1}GB 使用:{2}GB 剩餘:{3}GB 使用率:{4}%'.format(name, total, used, free, usage_rate));

def showNetword(receive, send, usage):
    print ('網路 接收:{0:.2f} 送出:{1:.2f} 使用:{2:.3f}'.format(receive/1024.*8, send/1024.*8, usage/1024.*8));

def startTask():
    get_device_name()
    get_device_mac_address()
    device_id = get_device_id()
    if(device_id == 0):
        print("connect fail")
        timedTask()
        return
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    showData()
    post_device_info(device_id)
    timedTask()

def timedTask():
    Timer(60, startTask, ()).start()

startTask()
