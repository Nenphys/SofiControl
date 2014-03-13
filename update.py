__author__ = 'Chapo'

import MySQLdb

db = MySQLdb.connect(host="localhost", user="admin", passwd="petrolog", db="sofi")
cursor = db.cursor(MySQLdb.cursors.DictCursor)
print("Python-MySQL connection: OK")

print(cursor.execute("UPDATE Eventos SET tx=0"))
cursor.close ()
db.commit ()