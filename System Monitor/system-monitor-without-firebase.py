import time
import psutil
import socket

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

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def cpu():
    cpu_core = psutil.cpu_count(logical=False);
    cpu_threads = psutil.cpu_count(logical=True);
    cpu_usage_rate = psutil.cpu_percent(interval=1, percpu=True)

    
    doc['cpu']['core'] = cpu_core;
    doc['cpu']['threads'] = cpu_threads;
    doc['cpu']['usage_rate'] = cpu_usage_rate;

def memory():
    memory_free = round(psutil.virtual_memory().free/(1024.0*1024.0*1024.0), 2);
    memory_total = round(psutil.virtual_memory().total/(1024.0*1024.0*1024.0), 2);
    memory_usage_rate = round((memory_total-memory_free)/memory_total, 2)*100;

    doc['memory']['total'] = memory_total;
    doc['memory']['free'] = memory_free;
    doc['memory']['usage_rate'] = memory_usage_rate;

def disk():
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

def network():
    net = psutil.net_io_counters();
    bytes_receive = net.bytes_recv;
    bytes_sent = net.bytes_sent;

    bytes_all = bytes_receive + bytes_sent;
    time.sleep(1);
    bytes_usage = bytes_receive + bytes_sent - bytes_all;

    doc['network']['receive'] = bytes_receive;
    doc['network']['send'] = bytes_sent;
    doc['network']['usage'] = bytes_usage;

def convert_to_gbit(value):
    return value/1024./1024.*8

def send_stat(value):
    print ("%0.3fMpbs" % convert_to_gbit(value))

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
    print ('網路 接收:{0:.2f} 送出:{1:.2f} 使用:{2:.3f}'.format(receive/1024./1024, send/1024./1024, usage/1024./1024.*8));


cpu();
memory();
disk();
network();

print (get_host_ip())
showData();