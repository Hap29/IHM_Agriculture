import mysql.connector
import datetime

db = mysql.connector.connect(host="localhost",user="admin",password="mot_de_passe", database="r2energie")

cur = db.cursor()
sql = "SELECT HUMIDITEAIR, TEMPERATUREAIR, ENSOLEILLEMENT,DATE,HEURE FROM DATAS_DEVICE"
cur.execute(sql) 

res = cur.fetchall()

print(type(res),"\n")

for line in res:
    print(line)
    