import pymssql

conn = pymssql.connect(server='(local)', user='python', password='1779', database='Northwind') 
cursor = conn.cursor()
cursor.execute('SELECT * FROM Employees')
row = cursor.fetchone()  
while row:  
 print("ID=%d, Name=%s" % (row[0], row[1]))     
 row = cursor.fetchone()  
conn.close()