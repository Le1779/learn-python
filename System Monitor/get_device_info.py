import pymssql
conn = pymssql.connect(server='10.0.0.55', user='DFO_Trial', password='DynaCW999', database='SystemMonitor')
cursor = conn.cursor()
cursor.execute('SELECT * FROM DeviceInfo')
row = cursor.fetchone()  
while row:  
 print("CPUInfo=%s, MemoryInfo=%s" % (row[0], row[1]))     
 row = cursor.fetchone()  
conn.close()