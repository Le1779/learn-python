import pymssql
import json
import datetime
import socket
import requests
from uuid import getnode as get_mac

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

device_name = '';
device_mac_address = '';
def get_device_name():
    global device_name
    device_name = socket.gethostname()

def get_device_mac_address():
    global device_mac_address
    device_mac_address = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))

def get_device_id():
    get_device_name()
    get_device_mac_address()
    post_data = {'name':device_name,'macAddress':device_mac_address}
    r = requests.post('http://dfo.dynacw.com:57555/Device/GetDeviceId', data = post_data)
    if r.status_code == requests.codes.ok:
        return r.json()['id']
    else:
        return 0

def analysisCPU(cpuJson):
    cpu = json.loads(cpuJson)
    doc['cpu']['core'] = cpu['core'];
    doc['cpu']['threads'] = cpu['threads'];
    doc['cpu']['usage_rate'] = cpu['usage_rate'];

def analysisMemory(memoryJson):
    memory = json.loads(memoryJson)
    doc['memory']['total'] = memory['total'];
    doc['memory']['free'] = memory['free'];
    doc['memory']['usage_rate'] = memory['usage_rate'];

def analysisDisk(diskJson):
    disk = json.loads(diskJson)
    doc['disk'] = disk;
    
def analysisNetwork(networkJson):
    network = json.loads(networkJson)
    doc['network']['receive'] = network['receive'];
    doc['network']['send'] = network['send'];
    doc['network']['usage'] = network['usage'];

def showData():
    showCPUInfo(doc['cpu']['core'], doc['cpu']['threads'])
    for i in range(len(doc['cpu']['usage_rate'])):
        showCPUUsageRate(i, doc['cpu']['usage_rate'][i]);
    
    showMemoryInfo(doc['memory']['total'], doc['memory']['free'], doc['memory']['usage_rate']);

    for diskInfo in doc['disk']:
        showDiskInfo(diskInfo['name'], diskInfo['total'], diskInfo['used'], diskInfo['free'], diskInfo['usage_rate']);
    
    showNetwork(doc['network']['receive'], doc['network']['send'], doc['network']['usage']);

def showCPUInfo(core, threads):
    print ('CPU {0}核{1}線程'.format(core, threads));

def showCPUUsageRate(threads, usage_rate):
    print ('CPU {0}線程使用率: {1}%'.format(threads, usage_rate));

def showMemoryInfo(total, free, usage_rate):
    print ('記憶體 總共:{0}GB 剩餘:{1}GB 使用率:{2}%'.format(total, free, usage_rate));

def showDiskInfo(name, total, used, free, usage_rate):
    print ('硬碟{0} 總共:{1}GB 使用:{2}GB 剩餘:{3}GB 使用率:{4}%'.format(name, total, used, free, usage_rate));

def showNetwork(receive, send, usage):
    print ('網路 接收:{0:.2f} 送出:{1:.2f} 使用:{2:.3f}'.format(receive/1024./1024, send/1024./1024, usage/1024./1024.*8));

conn = pymssql.connect(server='10.0.0.55', user='DFO_Trial', password='DynaCW999', database='SystemMonitor')
cursor = conn.cursor()
endDate = datetime.datetime.now()
startDate = endDate - datetime.timedelta(0, 180)
print(startDate.strftime("%Y/%m/%d %H:%M:%S"))
print(endDate.strftime("%Y/%m/%d %H:%M:%S"))
cursor.execute("SELECT * FROM DeviceInfo WHERE DeviceID = '" + str(get_device_id()) + "' AND UpdateTime BETWEEN '" + startDate.strftime("%Y/%m/%d %H:%M:%S") + "' AND '" + endDate.strftime("%Y/%m/%d %H:%M:%S") + "'")

tempRow = cursor.fetchone()  
row = tempRow
while tempRow:  
    row = tempRow
    tempRow = cursor.fetchone()  

analysisCPU(row[2])
analysisMemory(row[3])
analysisDisk(row[4])
analysisNetwork(row[5])
showData();   
conn.close()




