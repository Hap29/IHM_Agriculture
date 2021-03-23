import mysql.connector
import datetime
import time
import random

#db = mysql.connector.connect(host="192.168.0.201",user="admin",password="mot_de_passe", database="r2energie")    # @IP_LYCEE  
db = mysql.connector.connect(host="localhost",user="admin",password="mot_de_passe", database="r2energie")      # @IP_MAISON

cur = db.cursor()
sql = "INSERT INTO MODE_AUTO (idMODE_AUTO,LED,CHAUFFAGE,ARROSOIR ) VALUES (%s, %s,%s,%s)"
value = (1,5,5,5)
cur.execute(sql,value) 
db.commit()

"""
i = 0
while(i< 30) :
    date = str(datetime.date.today())
    heure = str(datetime.datetime.now().strftime("%H:%M:%S"))
    value = (random.randint(55,60), random.randint(20, 22),random.randint(20, 22), random.randint(55,60), random.randint(500, 800),  date, heure )
    i += 1
    cur.execute(sql,value) 
    db.commit()
    time.sleep(0.1)
"""
    


