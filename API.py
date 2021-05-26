#!/usr/bin/python3
#coding: utf-8
########################################################
#### ©EmmanuelBOURHIS, 2021, BTS SN IR , LCR, BREST ####
########################################################
####
from flask import redirect,url_for,session
import requests as req
import json 
import datetime 
import mysql.connector
import base64
from hashlib import blake2b
####
####
class identification:
	####CONNEXION A LA BDD AVEC MYSQL CONNECTOR
	def conndb():
		return mysql.connector.connect(host="XXXX",user="XX",password="XX", database="XX") #/!\ce n'est pas un user de la base mais admin de mysql
	####
	#### RETOURNE LE PARAMETRE EN STR ASSOCIE A L'ID DE LA PAGE
	def idnom(id):
		if  (id == 1):
			return "LED"
		elif(id == 2):
			return "CHAUFFAGE"
		elif(id == 3):
			return "ARROSOIR"
	####
	#### RETOURNE LE PARAMETRE EN STR ASSOCIE A L'ID DE LA PAGE
	def idlettre(id):
		if  (id == 1):
			return "L"
		elif(id == 2):
			return "C"
		elif(id == 3):
			return "A"
	#### RETOURNE LE PARAMETRE EN INT ASSOCIE A L'ID DE LA PAGE
	def idnombre(id):
		if  (id == "L"):
			return 1
		elif(id == "C"):
			return 2
		elif(id == "A"):
			return 3		
	#### RETURN l'ID DE REGLAGE AVEC SA VALEUR ASSCOCIEE
	def id(r,c,a) :
		if(float(r) >=0 ):
			return r,  1
		elif(float(c) >= 0 ):
			return c , 2
		elif(float(a) >=0):
			return a , 3
	####
####
####
class datas:
	####
	####  URL DOWNLINK DU TTN
	url_ttn = 'XXXXXXX'
	####
	#### CONFIGURATION DE LA RECUPERATION ENDPOINT
	def apipoint(rd) :
		Json = json.loads(rd.decode("utf_8"))                                      					#DECODAGE POUR CREER UN DICTIONNAIRE PYTHON
		payload_humair  = Json["payload_fields"]["humiditeair"]                    					#RECUPERATION DES DIFFERENTES DONNEES RECUES 
		payload_tempair = Json["payload_fields"]["temperatureair"] 
		payload_humsol  = Json["payload_fields"]["humiditesol"]  
		payload_tempsol = Json["payload_fields"]["temperaturesol"] 
		payload_soleil  = Json["payload_fields"]["ensoleillement"]
		return payload_humair, payload_tempair, payload_tempsol, payload_humsol, payload_soleil
	####
	####ECRITURE DANS LA BDD DES VALEURS ACQUISES AVEC DATE ET HEURE
	def envoisql(humair,tempair,tempsol,humsol,soleil):
		db = identification.conndb()                 		 #CONNEXION A LA BDD GRACE A LA FONCTION conndb()
		cur = db.cursor()			 		 #CREATION D'UN CURSEUR DANS LA BDD (sert a effectuer les actions sql)
		sql = "INSERT INTO DATAS_DEVICE (HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT,DATE,HEURE) VALUES (%s, %s,%s, %s,%s,%s,%s)"  #REQUETE SQL
		date = str(datetime.date.today())   						   #RECUPERATION DE LA DATE DU JOUR
		heure = str(datetime.datetime.now().strftime("%H:%M:%S"))      #RECUPERATION DE L'HEURE ACTUELLE
		value = (humair, tempair,tempsol,humsol, soleil, date, heure ) #ENTREE DES VALEURS DANS L'ORDRE DE CORRESPONDANCE SQL 
		cur.execute(sql,value) 										   #EXECUTION DE LA REQUETE SQL AVEC LE CURSEUR
		db.commit()													   #VALIDATION DE LA TRANSACTION
		db.close()													   #FERMETURE DE LA CONNEXION A LA BASE
		return "Envoi ok"											   #RETOUR OK (pour debug seulement)
	####
	#### ENTREE D'UN HISTORIQUE DES REGLAGES
	def entreglageval(val , id, besoinretour):
		req = identification.idnom(id)
		db = identification.conndb()                 		 #CONNEXION A LA BDD GRACE A LA FONCTION conndb()
		cur = db.cursor()			 		 #CREATION D'UN CURSEUR DANS LA BDD (sert a effectuer les actions sql)
		sql = "INSERT INTO H_REGLAGE ("+req+",HEURE,DATE) VALUES (%s,%s,%s)"  #REQUETE SQL
		date = str(datetime.date.today())   						   #RECUPERATION DE LA DATE DU JOUR
		heure = str(datetime.datetime.now().strftime("%H:%M:%S"))      #RECUPERATION DE L'HEURE ACTUELLE
		cur.execute(sql, (val,heure,date)) 										   #EXECUTION DE LA REQUETE SQL AVEC LE CURSEUR
		db.commit()													   #VALIDATION DE LA TRANSACTION
		db.close()													   #FERMETURE DE LA CONNEXION A LA BASE
		if(besoinretour == 1):
			page = "/commande"+identification.idlettre(id)
			return redirect(page)
	####
	#### RETOUR DE L'HISTORIQUE DE REGLAGE DE LA PAGE DEMANDE
	def visuvallreglage(id):
		req = identification.idnom(id)
		db = identification.conndb() 		
		cur = db.cursor()
		cur.execute("SELECT "+req+" FROM NB_L_AFF ")
		nbbd = cur.fetchall()
		nbbd = nbbd[0][0]		
		cur.execute("SELECT "+req+",HEURE,DATE FROM H_REGLAGE WHERE "+req+" IS NOT NULL ORDER BY idH_REGLAGE DESC LIMIT "+str(nbbd)+"") 
		res = cur.fetchall()
		db.close()
		return res
	####
	####ENVOI DE LA DONNEE DE REGLAGE
	def reglage(ent, id) : 
		ent = float(ent)   											   #CONVERSION DE LA CHAINE DE CHARACTERES EN NOMBRE REEL
		ent = int((ent * 255) / 10)									   #CONVERSION EN INTEGER DU NOMBRE APPROCHEE POUR UN OCTECT A PARTIR DE 10 VALEURS
		convb = bytes([id,ent])										   #RETOURNE UN OBJECT D'OCTECTS
		convb64 = base64.b64encode(convb)							   #ENCODE EN BASE 64 LA VALEUR RECUPEREE ET CONVERTIE CI-DESSUS
		payload = convb64.decode('utf-8')							   #DECODAGE DE LA CONVERSION EN UTF-8 POUR L'ENVOI D'UNE CHAINE DE CHARACTERES
		post = {"dev_id": "controleur1", "port": 1,"payload_raw": payload }    #DONNEES POUR LE TTN SOUS FORME REQUISE POUR TTN
		req.post( datas.url_ttn , json = post) 					           #ENVOI DE LA TRAME						
	####
	####RECUPERATION DES 20 DERNIERE DONNEE DE LA BASE POUR LE GRAPHIQUE
	def sqlgraph():
		db = identification.conndb()   											#CONNEXION A LA BDD GRACE A LA FONCTION conndb()
		cur = db.cursor()											#CREATION D'UN CURSEUR DANS LA BDD (rappel : sert a effectuer les actions sql)
		cur.execute("SELECT HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT,DATE,HEURE FROM DATAS_DEVICE ORDER BY idDATAS_DEVICE DESC LIMIT 20") #REQUETE SQL
		res = cur.fetchall()										#RECUPERATION DES DONNEES
		db.close()													#FERMETURE DE LA CONNEXION A LA BDD
		tempair = []												#TABLEAU DE VARIABLES DU GRAPHIQUE
		tempsol = []
		humair  = []
		humsol  = []
		enso    = []
		date    = []
		time    = []
		for i in res :											   #CORRESPONDANCE DES VALEURS RECUES AVEC LE SQL DANS LES TABLEAUX RESPECTIFS
			humair.append(i[0])
			tempair.append(i[1])
			tempsol.append(i[2])
			humsol.append(i[3])
			enso.append(i[4])
			date.append(i[5])
			time.append(i[6])
		return humair,tempair,tempsol,humsol,enso,time            #RETOUR DES TABLEAUX DE VALEURS POUR LES POINTS DES GRAPHIQUES
	####
	####RECUPERATION DE L'HEURE A UN MOMENT T
	def tempfixe():
		date = datetime.datetime.now()						      #RECUPERATION DE LA DATE ET L'HEURE
		h = str(date.hour)										  #RECUPERATION DE L'HEURE ET CONVERTION EN CHAINE DE CHARACTERE
		m = str(date.minute)									  #RECUPERATION DES MINUTES ET CONVERTION EN CHAINE DE CHARACTERE
		s = str(date.second)									  #RECUPERATION DES SECONDES ET CONVERTION EN CHAINE DE CHARACTERE
		heure =  h +":"+m+":"+s 								  #ASSEMBLAGE DE LA CHAINE DE CHARACTERE
		return heure											  #RETOUR DE L'HEURE (moment ou la fonction a ete appelle)
	####	
	####RECUPERATION DE LA DERNIERE VALEUR ENREGISTREE
	def sqldernier(): 
		db = identification.conndb()										      #CONNEXION A LA BDD GRACE A LA FONCTION conndb()
		cur = db.cursor()										  #CREATION D'UN CURSEUR DANS LA BDD (rappel : sert a effectuer les actions sql)
		cur.execute("SELECT HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT FROM DATAS_DEVICE ORDER BY idDATAS_DEVICE DESC LIMIT 1") #REQUETE SQL
		res = cur.fetchall()									  #RECUPERATION DES DONNEES DE LA DERNIERE COMMANDE
		db.close()												  #FERMETURE DE LA CONNEXION A LA BASE
		for i in res:											  #CORRESPONDANCE DES VALEURS DE LA BDD AUX VARIABLES A RENVOYER 
			humiair = i[0]
			tempair = i[1]
			tempsol = i[2]
			humisol = i[3]
			soleil  = i[4]
		return humiair,tempair,tempsol,humisol,soleil			  #DERNIERES VALEURS A AFFICHER DANS LA PAGE PRINCIPALE 
	####
	#### VISUALISATION SI COMMANDE MANUEL OU AUTO D'UN SEUL TYPE
	def sqlvisucommande(id = -1) :
		if(id != -1):
			req = identification.idnom(id)
			db = identification.conndb()
			cur = db.cursor()
			cur.execute("SELECT "+req+" FROM TYPE_COMMANDE")
			res = cur.fetchall()
			db.close()																							
			for i in res :
				typ = (i[0])
			if(int(typ) == 0):
				return "manuel"
			else:
				return "auto"
		else:
			condb = identification.conndb()
			cur = condb.cursor()
			cur.execute("SELECT LED,CHAUFFAGE,ARROSOIR FROM TYPE_COMMANDE ORDER BY idCOMMANDE DESC LIMIT 1")
			res = cur.fetchall()
			condb.close()
			return res
	####
	#### FONCTION APPUI SUR LE BOUTTON ET CHANGEMENT D'ETAT
	def changement_etat(id):
		req = identification.idnom(id)
		db = identification.conndb()
		cur = db.cursor()
		if(datas.sqlvisucommande(id) == 'manuel'):
			commande = 1
		else:
			commande = 0
		sql = "UPDATE TYPE_COMMANDE SET "+req+"="+str(commande)+""
		cur.execute(sql)
		db.commit()
		db.close()
		page = "/commande"+identification.idlettre(id)
		return redirect(page)
	####
	#### FONCTION  CHANGEMENT ETAT AFFICHAGE
	def changement_aff(id,nb):
		req = identification.idnom(id)
		db = identification.conndb()
		cur = db.cursor()
		chaine = "UPDATE NB_L_AFF SET "+req+"="+str(nb)+""
		cur.execute(chaine)
		db.commit()
		db.close()
		page = "/commande"+identification.idlettre(id)
		return redirect(page)
	####
	####
	def entreeseuils(id,dic):
		db = identification.conndb()
		cur = db.cursor()
		sql = "UPDATE MODE_AUTO SET S_TEMPAIR = %s ,S_TEMPSOL= %s,S_HUMAIR= %s,S_HUMSOL= %s,S_SOLEIL = %s WHERE idMODE_AUTO = "+str(id)+""
		value = (dic['tempair'],dic['tempsol'],dic['humair'],dic['humsol'],dic['enso'])
		cur.execute(sql,value) 
		db.commit()
		db.close()
	####
	####
	def entreeconditions(id,dic):
		db = identification.conndb()
		if (dic['type-reg'] == "fixe"):
			ty = "0"
		else:
			ty = "1"
		cur = db.cursor()
		sql = "UPDATE MODE_AUTO SET R_FIXE_DESSOUS = %s ,R_FIXE_DESSUS= %s,PALIER_NFIX= %s,D_LUX= %s,TYPE_REG = %s WHERE idMODE_AUTO = "+str(id)+""
		value = (dic['fixdessous'],dic['fixdessus'],dic['palier'],dic['dlux'], ty)
		cur.execute(sql,value) 
		db.commit()
		db.close()
	####
	####
	def pageregmode():
		db = identification.conndb()
		cur = db.cursor()
		sql = "SELECT idMODE_AUTO,S_TEMPAIR,S_TEMPSOL,S_HUMAIR,S_HUMSOL,S_SOLEIL,R_FIXE_DESSOUS,R_FIXE_DESSUS,PALIER_NFIX,D_LUX,TYPE_REG FROM MODE_AUTO"
		cur.execute(sql) 
		res = cur.fetchall()
		idx = 0
		lreg = []
		for i in res:
			ty = i[10]
			#print(ty)
			if(ty == "1"):
				lreg.extend(["","checked"])
			else:
				lreg.extend(["checked",""])
			idx+=1
		return res,lreg
	####
	####
	def encrypt(aenc,taille = 16):
		####SHA256 online hash function pour la clé
		h = blake2b(digest_size = taille, key = b'XXXXXXXXXXXXXXX')   # h est la configuration pour l'encodage de blacke2b Clef secrete en bytes  on peut aussi ecrire bytes( 'emmanuel' , encoding = (utf-8))
		h.update(aenc) # encrypte la donnée mdp
		return h.hexdigest().encode('utf-8')   # Renvoie le digest des données passées à la méthode en hexa, encode en utf8 pour etre lu
	####
	####
	def bddlogin(login="",mdp=""):
		conn = False
		adm = False
		userok = False
		logc = ""
		db = identification.conndb()
		cur = db.cursor()
		sql = "SELECT LOGIN,MDP,PRIVILEGE FROM UTILISATEUR"
		cur.execute(sql)
		res = cur.fetchall()
		login = bytes(login,encoding=('utf-8'))
		mdp   = bytes(mdp,encoding=('utf-8'))
		for i in res:
			if (str(datas.encrypt(login),encoding=('utf-8')) == i[0] and str(datas.encrypt(mdp),encoding=('utf-8')) == i[1]):
				if( i[2] == "fb19"):
					adm = True
				conn = True
				break
			elif ((str(datas.encrypt(login),encoding=('utf-8')) == i[0])):
				logc  = str(datas.encrypt(login),encoding=('utf-8'))
				userok = True
		return conn,adm,res, logc, userok
	####
	####
	def bddatt(user,passw):
		db = identification.conndb()
		cur = db.cursor()
		sql = "INSERT INTO ALERTES (NOM_COMPTE_ATTAQUE,MDP_ESSAYE,D_H) VALUES (%s,%s,%s)"
		user  =  str(datas.encrypt(bytes(user ,encoding=('utf-8'))), encoding=('utf-8'))
		passw = str(datas.encrypt(bytes(passw ,encoding=('utf-8'))), encoding=('utf-8'))
		cur.execute(sql,(user,passw,datetime.datetime.now()))
		db.commit()
		db.close
	####
	####
	def suppuser(user):
		db = identification.conndb()
		cur = db.cursor()
		sql = "DELETE FROM UTILISATEUR where LOGIN ='"+str(user)+"'"
		cur.execute(sql)
		db.commit()
		db.close()
	####
	####
	def upmdp(user,mdp):
		db = identification.conndb()
		cur = db.cursor()
		sql = "UPDATE UTILISATEUR SET MDP = '"+str(datas.encrypt(bytes(mdp,encoding=('utf-8'))), encoding=('utf-8'))+"' where LOGIN ='"+str(user)+"'"
		cur.execute(sql)
		db.commit()
		db.close()
	####
	####
	def adduser(login,mdp,priv):
		db = identification.conndb()
		cur = db.cursor()
		sql = "INSERT INTO UTILISATEUR (LOGIN,MDP,PRIVILEGE) VALUES (%s,%s,%s)"
		login = str(datas.encrypt(bytes(login ,encoding=('utf-8'))), encoding=('utf-8'))
		mdp   = str(datas.encrypt(bytes(mdp   ,encoding=('utf-8'))), encoding=('utf-8'))
		priv  = str(datas.encrypt(bytes(priv  ,encoding=('utf-8')),2), encoding=('utf-8'))
		cur.execute( sql , (login,mdp,priv) )
		db.commit()
		db.close
####
####
class erreur:
	def attention():
		attention = """
				###################
				#### ATTENTION ####
				###################
				"""
		return attention
	####
	####
	def messageatt():
		warm = """
			###################################
			#### NE PAS ARRETER LE SERVEUR ####
			###################################
			"""
		return warm
	####
	####

