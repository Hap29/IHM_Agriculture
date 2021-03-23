import mysql.connector
import datetime

db = mysql.connector.connect(host="192.168.0.44",user="admin",password="mot_de_passe", database="r2energie")

cur = db.cursor()
sql = "SELECT HUMIDITE, TEMPERATURE, ENSOLEILLEMENT,DATE,HEURE FROM DATAS_DEVICE"
cur.execute(sql) 

res = cur.fetchall()

print(type(res),"\n")

print(res[0])

"""
for line in res:
    print(line)
    """