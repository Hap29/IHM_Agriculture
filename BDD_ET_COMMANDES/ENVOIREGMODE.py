import mysql.connector
import datetime
import time
import random

#db = mysql.connector.connect(host="192.168.0.201",user="admin",password="mot_de_passe", database="r2energie")    # @IP_LYCEE  
db = mysql.connector.connect(host="localhost",user="admin",password="mot_de_passe", database="r2energie")      # @IP_MAISON

cur = db.cursor()
sql = "INSERT INTO MODE_AUTO (idMODE_AUTO,S_TEMPAIR,S_TEMPSOL,S_HUMAIR,S_HUMSOL,S_SOLEIL,R_FIXE_DESSOUS,R_FIXE_DESSUS,PALIER_NFIX,D_LUX,TYPE_REG) VALUES (%s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s)"


value = (3,20,20,30,30,50,5,5,0.1,5,0)
cur.execute(sql,value) 
db.commit()
