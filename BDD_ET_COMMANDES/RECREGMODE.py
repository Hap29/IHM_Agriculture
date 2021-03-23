import mysql.connector
import datetime

db = mysql.connector.connect(host="192.168.0.201",user="admin",password="mot_de_passe", database="r2energie")


cur = db.cursor()
sql = "SELECT idMODE_AUTO,S_TEMPAIR,S_TEMPSOL,S_HUMAIR,S_HUMSOL,S_SOLEIL,R_FIXE_DESSOUS,R_FIXE_DESSUS,PALIER_NFIX,D_LUX,TYPE_REG FROM MODE_AUTO"
cur.execute(sql) 
res = cur.fetchall()

print(type(res),"\n")

for line in res:
    print(line)

print(":::::::::::::::::")
print(res[0][0])
    